#!/usr/bin/env python3
"""Pastel 2D card regeneration: Gemini on Vertex AI via ADC (global playbook).
Pairs with 25s sleep; single retry pass on failures. Overwrites assets/img/hf2d_*.png.
"""
import base64
import json
import time
import urllib.request
from pathlib import Path

import google.auth
from google.auth.transport.requests import Request

PROJECT = "project-d1f08481-a42a-483b-804"
LOCATION = "global"
MODEL = "gemini-3-pro-image"
URL = (f"https://aiplatform.googleapis.com/v1/projects/{PROJECT}/locations/{LOCATION}"
       f"/publishers/google/models/{MODEL}:generateContent")

OUT = Path(__file__).resolve().parent / "assets" / "img"

ANCHOR = ("premium flat 2D vector illustration for a modern fintech marketing site, "
          "soft pastel rendering with BLUE as the clear lead color: powder blue, sky "
          "blue, and cornflower blue dominate every scene, with tasteful small accents "
          "of blush pink, butter yellow, and soft mint on a warm off-white background, "
          "no purple, green never leads, gentle low-saturation tones, rounded "
          "geometric shapes, subtle film grain, clean minimal composition, "
          "no text, no words. ")

PROMPTS = {
    "hf2d_41_website": (ANCHOR + "square: friendly robotic arms on a small platform composing a website screen from typography blocks and image tiles", "1:1"),
    "hf2d_42_video": (ANCHOR + "square: glowing film-frame cards riding a small conveyor loop toward a cute projector head", "1:1"),
    "hf2d_43_deck": (ANCHOR + "square: a neat fan of presentation slides held by a little mechanical easel", "1:1"),
    "hf2d_44_document": (ANCHOR + "square: a small typesetting press pressing a glowing page, finished pages stacked beside it", "1:1"),
    "hf2d_45_research": (ANCHOR + "square: a telescope aimed at a floating constellation of small catalog cards", "1:1"),
    "hf2d_46_launch": (ANCHOR + "square: a small storefront kiosk with a striped awning being assembled by two robotic arms", "1:1"),
    "hf2d_47_social": (ANCHOR + "square: a tilted calendar grid of thirty small colorful tiles, a tiny robot polishing one", "1:1"),
    "hf2d_48_compete": (ANCHOR + "square: a lighthouse on a small rise sweeping its beam over terraced platforms holding miniature rival buildings", "1:1"),
    "hf2d_53_aivideo": (ANCHOR + "square: a film clapperboard surrounded by four small video frames materializing from sparkle particles", "1:1"),
    "hf2d_54_icp": (ANCHOR + "square: concentric target rings with a magnifying glass highlighting one segment of a crowd of abstract profile cards", "1:1"),
    "hf2d_49_model": (ANCHOR + "4:3: a single friendly compute core with cooling fins on a soft hill, small clouds", "4:3"),
    "hf2d_50_credits": (ANCHOR + "4:3: golden coins cascading from a little cloud through glass pipes into a collection machine", "4:3"),
    "hf2d_51_skills": (ANCHOR + "4:3: a cheerful robot librarian filing a glowing card into a tall organized card rack", "4:3"),
    "hf2d_52_fork": (ANCHOR + "wide: one conveyor belt splitting into eight smaller belts, each ending at a differently colored small pavilion, packages riding the belts", "3:2"),
    "hf2d_55_assembly": (ANCHOR + "wide: robotic arms over an assembly line composing a website screen from typography blocks and image tiles", "3:2"),
    "hf2d_56_loop": (ANCHOR + "wide: a circular conveyor refinement loop where screens pass a polishing station and emerge brighter, one exit ramp releasing a finished screen", "3:2"),
    "hf2d_57_archive": (ANCHOR + "wide: colorful archive shelving holding catalogued blocks, one block pulled out glowing with a small red wax seal", "3:2"),
    "hf2d_58_credits": (ANCHOR + "wide: golden coins cascading from a cloud through pastel glass pipes into a collection vault on a meadow", "3:2"),
}


def get_token():
    creds, _ = google.auth.default(scopes=["https://www.googleapis.com/auth/cloud-platform"])
    creds.refresh(Request())
    return creds.token


def gen(name, prompt, ar, token):
    body = {
        "contents": {"role": "USER", "parts": [{"text": prompt}]},
        "generationConfig": {"responseModalities": ["TEXT", "IMAGE"],
                             "imageConfig": {"aspectRatio": ar, "imageSize": "2K"}},
    }
    req = urllib.request.Request(URL, data=json.dumps(body).encode(), headers={
        "Authorization": f"Bearer {token}",
        "x-goog-user-project": PROJECT,
        "Content-Type": "application/json",
    })
    with urllib.request.urlopen(req, timeout=180) as r:
        data = json.load(r)
    for cand in data.get("candidates", []):
        for part in cand.get("content", {}).get("parts", []):
            if "inlineData" in part:
                (OUT / f"{name}.png").write_bytes(base64.b64decode(part["inlineData"]["data"]))
                return True
    return False


def main():
    token = get_token()
    items = list(PROMPTS.items())
    failed = []
    for i, (name, (prompt, ar)) in enumerate(items):
        try:
            ok = gen(name, prompt, ar, token)
        except Exception as e:
            ok = False
            print(f"{name}: ERROR {e}", flush=True)
        print(f"{name}: {'ok' if ok else 'FAIL'} ({i+1}/{len(items)})", flush=True)
        if not ok:
            failed.append(name)
        if i % 2 == 1:
            time.sleep(25)
        if i % 8 == 7:
            token = get_token()
    for name in list(failed):
        time.sleep(25)
        try:
            if gen(name, PROMPTS[name][0], PROMPTS[name][1], get_token()):
                failed.remove(name)
                print(f"{name}: ok on retry", flush=True)
        except Exception as e:
            print(f"{name}: retry ERROR {e}", flush=True)
    print(f"DONE: {len(items) - len(failed)}/{len(items)}; failed: {failed}", flush=True)


if __name__ == "__main__":
    main()
