#!/usr/bin/env python3
"""Batch 3: Gemini image gen on Vertex AI via ADC (per global playbook).
Pairs with 25s sleep; single-target retry on 429. Saves to assets/img/g{N}.png.
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
HOST = "aiplatform.googleapis.com"
URL = (f"https://{HOST}/v1/projects/{PROJECT}/locations/{LOCATION}"
       f"/publishers/google/models/{MODEL}:generateContent")

OUT = Path(__file__).resolve().parent / "assets" / "img"
OUT.mkdir(parents=True, exist_ok=True)

ANCHOR = ("ultra-clean 3D render in the style of premium Framer fintech "
          "templates: soft pastel dawn sky, lush rolling emerald-green hills, "
          "pristine white engineered structures, high-key natural light, "
          "minimal composition, no text, no words, no people. ")

PROMPTS = {
    # Square card art for the 8 harness cards on the tool page
    "g01_card_website": (ANCHOR + "square composition: robotic arms on a compact white assembly platform composing a glowing website screen from typography and image tiles", "1:1"),
    "g02_card_video": (ANCHOR + "square composition: glowing film-frame cards riding a small white conveyor loop toward a white projector head", "1:1"),
    "g03_card_deck": (ANCHOR + "square composition: a neat fan of glowing presentation slides held by a white mechanical easel", "1:1"),
    "g04_card_document": (ANCHOR + "square composition: a white typesetting press pressing a glowing page, stacked finished pages beside it", "1:1"),
    "g05_card_research": (ANCHOR + "square composition: a white telescope apparatus aimed at a floating constellation of tiny glowing catalog cards", "1:1"),
    "g06_card_launch": (ANCHOR + "square composition: a small pristine white storefront kiosk with awning being assembled by two robotic arms", "1:1"),
    "g07_card_social": (ANCHOR + "square composition: a tilted calendar grid of thirty small glowing tiles, a tiny white robot polishing one", "1:1"),
    "g08_card_compete": (ANCHOR + "square composition: a white watchtower on a green rise overlooking terraced platforms holding miniature rival structures", "1:1"),
    # Wide art
    "g09_hero_alt": (ANCHOR + "vast wide shot: a white elevated pipeline of glowing panels sweeping an S-curve through hills to the horizon, generous empty sky above", "16:9"),
    "g10_inputs_wide": (ANCHOR + "wide shot: three white pedestals evenly spaced on a green ridge holding a glowing compute cube, a vessel of golden energy, and a stack of glowing skill cards, the cards pedestal brightest", "16:9"),
    "g11_resources": (ANCHOR + "wide shot: golden luminous credit coins cascading through elegant white glass piping across a meadow into a white collection vault", "16:9"),
    "g12_scan_alt": (ANCHOR + "wide shot: white radar dish array at dawn on a hilltop, soft beams sweeping a valley of floating geometric artifacts", "16:9"),
    "g13_gate_wide": (ANCHOR + "wide shot: a white inspection gate straddling a conveyor on green hills, emerald beacon glowing, panels queueing", "16:9"),
    "g14_loop_wide": (ANCHOR + "wide shot: a white circular refinement loop conveyor on a hilltop, screens improving each pass, one exit ramp releasing a finished glowing screen", "16:9"),
    "g15_dark_cta": ("ultra-clean 3D render, dark premium fintech aesthetic, deep indigo night over rolling hills, a warm glowing white slab monument in the center foreground with faint amber flow lines converging into it, stars, minimal, no text, no people", "16:9"),
    "g16_og_card": (ANCHOR + "wide banner composition with the left half open empty meadow and soft sky for text overlay, right half a white pipeline curving away with glowing panels", "16:9"),
    "g17_archive_macro": (ANCHOR + "macro close-up: one white catalogued block half-pulled from a white shelf, glowing edge, tiny vermilion wax seal, shallow depth of field", "16:9"),
    "g18_fork_eight": (ANCHOR + "wide aerial: one white assembly line forking into eight branches across a valley, each branch ending at a distinct small white pavilion", "16:9"),
    "g19_hero_tall": (ANCHOR + "vertical composition: a white pipeline of glowing panels climbing terraced green hills toward a bright dawn sky", "9:16"),
    "g20_workflow_iso": (ANCHOR + "isometric view: a compact white factory diagram built as real architecture, five stations connected by conveyor paths with glowing pulses, on a green plateau", "16:9"),
    # Variants for choice
    "g21_hero_v3": (ANCHOR + "vast wide shot, low camera angle in wildflowers: white elevated conveyor pipeline overhead carrying glowing panels toward distant hills", "16:9"),
    "g22_inputs_v2": (ANCHOR + "wide shot: three glass display cases in a row on a green ridge: a compute cube, flowing golden energy, and stacked glowing cards, the third case open with light spilling out", "16:9"),
    "g23_dark_v2": ("ultra-clean 3D render, dark premium fintech aesthetic: night hills with an illuminated white flowchart network built across the terrain, soft amber pulses traveling the paths, stars, minimal, no text, no people", "16:9"),
    "g24_video_wide": (ANCHOR + "wide shot: a white outdoor editing suite structure with a large glowing timeline ribbon flowing through it like a river across the meadow", "16:9"),
    "g25_doc_wide": (ANCHOR + "wide shot: giant glowing manuscript pages on a white drying line across a green valley, a white press machine in the foreground", "16:9"),
    "g26_launch_wide": (ANCHOR + "wide shot: a white storefront kiosk at the center of a meadow crossroads, white paths radiating outward, small glowing envelope cards traveling the paths", "16:9"),
    "g27_social_wide": (ANCHOR + "wide shot: a month-long calendar boardwalk of glowing tiles winding over green hills, a small white robot placing the next tile", "16:9"),
    "g28_research_wide": (ANCHOR + "wide shot: a long white ledger table across a hillside covered in glowing catalog cards, a lens apparatus on rails inspecting them, some cards sealed with green checks", "16:9"),
    "g29_deck_wide": (ANCHOR + "wide shot: a gallery row of white easels on a lawn each holding a glowing slide, one central easel spotlit by dawn light", "16:9"),
    "g30_favicon_mark": ("minimal 3D render: a single pristine white square tile with three stacked horizontal glowing bars embossed on it, offset like layered rails, soft studio light on light gray background, centered, no text", "1:1"),
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
                (OUT / f"{name}.png").write_bytes(
                    base64.b64decode(part["inlineData"]["data"]))
                return True
    return False


def main():
    token = get_token()
    items = list(PROMPTS.items())
    done, failed = 0, []
    for i, (name, (prompt, ar)) in enumerate(items):
        if (OUT / f"{name}.png").exists():
            done += 1
            continue
        try:
            ok = gen(name, prompt, ar, token)
        except Exception as e:
            ok = False
            print(f"{name}: ERROR {e}", flush=True)
        if ok:
            done += 1
            print(f"{name}: ok ({done}/{len(items)})", flush=True)
        else:
            failed.append(name)
        if i % 2 == 1:
            time.sleep(25)
        if i % 10 == 9:  # refresh token occasionally
            token = get_token()
    # one retry pass for stragglers, singles with pacing
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
