#!/usr/bin/env python3
"""
Video Renderer for TikTok-style reels.
Generates a 9:16 MP4 video using the audio file and a TikTok concept JSON.
"""

from typing import Dict, Any, List, Tuple
import os
import math
import json
import random

import numpy as np
import librosa

# MoviePy layout in this environment
from moviepy.video.VideoClip import VideoClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy.video.VideoClip import ColorClip, ImageClip
from moviepy.audio.io.AudioFileClip import AudioFileClip

# Pillow for text rendering
from PIL import Image, ImageDraw, ImageFont

DEFAULT_SIZE = (1080, 1920)  # 9:16 portrait
DEFAULT_FPS = 30


def _safe_text(text: str, max_len: int = 140) -> str:
	if not text:
		return ""
	text = text.replace("\n", " ").strip()
	return (text[: max_len - 3] + "...") if len(text) > max_len else text


def _generate_dynamic_bg(size: Tuple[int, int], duration: float) -> VideoClip:
	w, h = size
	def make_frame(t: float):
		x = np.linspace(0, 1, w)
		y = np.linspace(0, 1, h)
		gx, gy = np.meshgrid(x, y)
		phase = 2 * math.pi * (t / max(0.01, duration))
		v = 0.5 + 0.5 * np.sin(2 * math.pi * (gx * 1.5 + gy * 1.2) + phase)
		# palette shift for more contrast
		r = np.clip(0.6 * v + 0.25, 0, 1)
		g = np.clip(0.25 * v + 0.05, 0, 1)
		b = np.clip(0.9 * v + 0.25, 0, 1)
		frame = np.stack([r, g, b], axis=2)
		return (frame * 255).astype("uint8")
	return VideoClip(make_frame, duration=duration)


def _beats_from_audio(audio_path: str, sr_target: int = 22050) -> List[float]:
	y, sr = librosa.load(audio_path, sr=sr_target, mono=True)
	tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
	return librosa.frames_to_time(beats, sr=sr).tolist()


def _pulse_overlay(size: Tuple[int, int], times: List[float], duration: float) -> VideoClip:
	w, h = size
	def make_frame(t: float):
		pulse = 0.0
		for bt in times:
			if abs(t - bt) < 0.10:
				pulse = max(pulse, 1.0 - (abs(t - bt) / 0.10))
		alpha = (pulse ** 2) * 0.35
		img = np.zeros((h, w, 3), dtype=np.uint8)
		val = int(alpha * 255)
		img[:, :, :] = (val, val, val)
		return img
	return VideoClip(make_frame, duration=duration)


def _render_text_image(text: str, box_size: Tuple[int, int], fontsize: int = 64, color: Tuple[int, int, int] = (255, 255, 255)) -> np.ndarray:
	w, h = box_size
	img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
	draw = ImageDraw.Draw(img)
	font = None
	for fpath in [
		"C:/Windows/Fonts/arialbd.ttf",
		"C:/Windows/Fonts/arial.ttf",
		"/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
		"/Library/Fonts/Arial Bold.ttf",
	]:
		if os.path.exists(fpath):
			try:
				font = ImageFont.truetype(fpath, fontsize)
				break
			except Exception:
				pass
	if font is None:
		font = ImageFont.load_default()

	text = _safe_text(text, 220)
	lines = []
	words = text.split()
	line = ""
	for wtoken in words:
		candidate = (line + " " + wtoken).strip()
		bbox = draw.textbbox((0, 0), candidate, font=font)
		if bbox[2] <= w - 20:
			line = candidate
		else:
			if line:
				lines.append(line)
			line = wtoken
	if line:
		lines.append(line)
	line_heights = []
	for ln in lines:
		bbox = draw.textbbox((0, 0), ln, font=font)
		line_heights.append(bbox[3] - bbox[1])
	total_h = sum(line_heights) + max(0, (len(lines) - 1)) * 8
	y_cursor = (h - total_h) // 2
	for ln, lh in zip(lines, line_heights):
		bbox = draw.textbbox((0, 0), ln, font=font)
		ln_w = bbox[2] - bbox[0]
		x = (w - ln_w) // 2
		for dx in (-2, 0, 2):
			for dy in (-2, 0, 2):
				draw.text((x + dx, y_cursor + dy), ln, font=font, fill=(0, 0, 0, 220))
		draw.text((x, y_cursor), ln, font=font, fill=(color[0], color[1], color[2], 255))
		y_cursor += lh + 8
	return np.array(img.convert("RGB"))


def _image_text_clip(text: str, size: Tuple[int, int], start: float, end: float, fontsize: int) -> ImageClip:
	img = _render_text_image(text, (int(size[0] * 0.9), 300), fontsize=fontsize)
	clip = ImageClip(img).with_start(start).with_duration(max(0.01, end - start))
	return clip.with_position(("center", int(size[1] * 0.12)))


def _typewriter_clip(text: str, size: Tuple[int, int], start: float, dur: float, fontsize: int = 72) -> VideoClip:
	text = _safe_text(text, 160)
	w, h = int(size[0] * 0.9), 280
	def make_frame_local(t: float):
		progress = max(0.0, min(1.0, t / max(0.01, dur)))
		n = max(1, int(len(text) * progress))
		img = _render_text_image(text[:n], (w, h), fontsize=fontsize, color=(255, 240, 200))
		canvas = np.zeros((size[1], size[0], 3), dtype=np.uint8)
		x0 = (size[0] - w) // 2
		y0 = int(size[1] * 0.18)
		canvas[y0:y0+h, x0:x0+w] = img
		return canvas
	return VideoClip(make_frame_local, duration=dur).with_start(start)


def _segment_timeline(duration: float) -> Dict[str, Tuple[float, float]]:
	intro_end = duration * 0.10
	hook_end = intro_end + duration * 0.10
	dev_end = hook_end + duration * 0.50
	climax_end = dev_end + duration * 0.20
	closing_end = duration
	return {
		"intro": (0.0, intro_end),
		"hook_moment": (intro_end, hook_end),
		"development": (hook_end, dev_end),
		"climax": (dev_end, climax_end),
		"closing": (climax_end, closing_end),
	}


def _waveform_overlay(size: Tuple[int, int], audio_path: str, duration: float) -> VideoClip:
	w, h = size
	y, sr = librosa.load(audio_path, sr=22050, mono=True)
	win = int(sr * 0.02)
	env = np.abs(librosa.util.frame(y, frame_length=win, hop_length=win).mean(axis=0))
	env = env / (env.max() + 1e-8)
	def make_frame(t: float):
		idx = int((t / max(0.01, duration)) * len(env))
		idx = np.clip(idx, 0, len(env) - 1)
		bar_w = int(w * 0.9)
		bar_h = 140
		img = np.zeros((bar_h, bar_w, 3), dtype=np.uint8)
		val = env[idx]
		filled = int(bar_w * val)
		img[:, :filled, :] = (200, 200, 255)
		canvas = np.zeros((h, w, 3), dtype=np.uint8)
		y0 = int(h * 0.78)
		x0 = int(w * 0.05)
		canvas[y0:y0+bar_h, x0:x0+bar_w] = img
		return canvas
	return VideoClip(make_frame, duration=duration)


def _karaoke_clips(transcription: str, size: Tuple[int, int], duration: float) -> List[ImageClip]:
	clips: List[ImageClip] = []
	text = _safe_text(transcription, 400)
	if not text:
		return clips
	parts = []
	for seg in text.split('.'):
		seg = seg.strip()
		if len(seg) > 3:
			parts.append(seg)
	if not parts:
		parts = [text]
	per = duration / len(parts)
	start = 0.0
	for seg in parts:
		end = min(duration, start + per)
		img = _render_text_image(seg, (int(size[0]*0.9), 200), fontsize=56, color=(255, 235, 140))
		clip = ImageClip(img).with_start(start).with_duration(end - start).with_position(("center", int(size[1]*0.86)))
		clips.append(clip)
		start = end
	return clips


def render_tiktok_reel(concept: Dict[str, Any], audio_path: str, output_path: str, size: Tuple[int, int] = DEFAULT_SIZE, fps: int = DEFAULT_FPS, wow: bool = False, transcription: str = "") -> str:
	if not os.path.exists(audio_path):
		raise FileNotFoundError(f"Audio not found: {audio_path}")
	audio_clip = AudioFileClip(audio_path)
	duration = float(getattr(audio_clip, "duration", 0.0))
	if not duration or duration <= 0:
		duration = 30.0
	bg = _generate_dynamic_bg(size, duration)
	beats = []
	try:
		beats = _beats_from_audio(audio_path)
	except Exception:
		beats = []
	pulse = _pulse_overlay(size, beats, duration) if beats else ColorClip(size, color=(0, 0, 0)).with_opacity(0)

	story = concept.get("story_structure", {})
	timeline = _segment_timeline(duration)

	layers: List[VideoClip] = [bg, pulse]
	def add_text_at(text: str, start: float, end: float, fontsize: int = 68):
		if not text:
			return
		layers.append(_image_text_clip(text, size, start, end, fontsize))

	# kinetic title intro
	intro_end = min(2.8, duration)
	ttl = concept.get("concept_title") or ""
	if ttl:
		layers.append(_typewriter_clip(ttl, size, 0.0, intro_end, fontsize=80))
	else:
		add_text_at("ReelSense AI", 0, intro_end, fontsize=80)

	# rest of structure
	add_text_at(story.get("hook_moment"), *timeline["hook_moment"]) if "hook_moment" in story else None
	add_text_at(story.get("development"), *timeline["development"]) if "development" in story else None
	add_text_at(story.get("climax"), *timeline["climax"]) if "climax" in story else None
	add_text_at(story.get("closing"), *timeline["closing"]) if "closing" in story else None

	hashtags = concept.get("hashtags") or []
	if hashtags:
		ht_text = "  ".join([f"#{h.lstrip('#')}" for h in hashtags[:5]])
		ht_img = _render_text_image(ht_text, (int(size[0]*0.9), 160), fontsize=44)
		layers.append(ImageClip(ht_img).with_position(("center", int(size[1]*0.92))).with_start(0).with_duration(duration))

	if wow:
		layers.append(_waveform_overlay(size, audio_path, duration))
		layers.extend(_karaoke_clips(transcription, size, duration))

	video = CompositeVideoClip(layers, size=size).with_audio(audio_clip).with_duration(duration)
	os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
	video.write_videofile(output_path, fps=fps, codec="libx264", preset="medium", audio_codec="aac", threads=4)
	video.close()
	audio_clip.close()
	return output_path


def main():
	import argparse
	parser = argparse.ArgumentParser(description="Render TikTok reel video from concept JSON and audio")
	parser.add_argument("audio", help="Path to audio file")
	parser.add_argument("concept_json", help="Path to concept JSON (either a concept dict or integrated results with tiktok_concepts)")
	parser.add_argument("--output", "-o", default="outputs/reel.mp4", help="Output MP4 path")
	parser.add_argument("--wow", action="store_true", help="Enable WOW pack: waveform + karaoke + beat sync + typewriter")
	args = parser.parse_args()

	with open(args.concept_json, "r", encoding="utf-8") as f:
		data = json.load(f)

	concept = data
	transcription = ""
	if isinstance(data, dict) and "tiktok_concepts" in data:
		concepts = data.get("tiktok_concepts") or []
		if not concepts:
			raise ValueError("No concepts found in provided JSON. Run the TikTok generator first.")
		concept = concepts[0]
		transcription = data.get("transcription", "")

	out = render_tiktok_reel(concept, args.audio, args.output, wow=args.wow, transcription=transcription)
	print(f"✅ Reel generado: {out}")

if __name__ == "__main__":
	main()
