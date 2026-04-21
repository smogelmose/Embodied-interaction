#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Metamorphic Efforts -- Effort perception questionnaire
PsychoPy 2023.x
Uses visual.Slider (no legacy plugins required).
"""

from psychopy import visual, event, core, gui
import os, csv, datetime

# ---------------------------------------------------------------------------
# Participant dialog
# ---------------------------------------------------------------------------
exp_info = {"Participant": "", "Session": "001"}
dlg = gui.DlgFromDict(exp_info, title="Metamorphic Efforts",
                      order=["Participant", "Session"])
if not dlg.OK:
    core.quit()

timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
os.makedirs("data", exist_ok=True)
outfile = "data/ME_P{}_S{}_{}.csv".format(
    exp_info["Participant"], exp_info["Session"], timestamp)

# ---------------------------------------------------------------------------
# Window
# ---------------------------------------------------------------------------
win = visual.Window(
    size=[1280, 800], fullscr=False,
    color=[0.92, 0.92, 0.90], colorSpace="rgb",
    units="norm", winType="pyglet"
)

# ---------------------------------------------------------------------------
# Reusable static stims (created once, reused)
# ---------------------------------------------------------------------------
stim_title = visual.TextStim(win, text="", pos=(0, 0.92), height=0.052,
    color=(-0.85, -0.85, -0.85), bold=True, wrapWidth=1.7,
    font="Helvetica", anchorHoriz="center", anchorVert="center")

stim_instr = visual.TextStim(win,
    text="Rate based on your overall embodied experience of this section.",
    pos=(0, 0.82), height=0.034, color=(-0.6, -0.6, -0.6),
    wrapWidth=1.6, font="Helvetica",
    anchorHoriz="center", anchorVert="center")

stim_cont = visual.TextStim(win,
    text="Press SPACE to continue", pos=(0, -0.90), height=0.042,
    color=(-0.5, -0.5, -0.5), font="Helvetica",
    anchorHoriz="center", anchorVert="center")

stim_warn = visual.TextStim(win,
    text="Rate all four scales before continuing.",
    pos=(0, -0.90), height=0.042, color=(0.5, -0.3, -0.3),
    font="Helvetica", anchorHoriz="center", anchorVert="center")

dividers = []
for i in range(1, 6):
    dividers.append(visual.TextStim(win, text="-" * 60,
        pos=(0, 0), height=0.014, color=(-0.80, -0.80, -0.80),
        font="Helvetica", anchorHoriz="center", anchorVert="center"))

stim_emotion_label = visual.TextStim(win, text="Your emotional response:",
    pos=(0, -0.30), height=0.028, color=(-0.4, -0.4, -0.4),
    italic=True, font="Helvetica",
    anchorHoriz="center", anchorVert="center")

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def txt(text, pos=(0, 0), height=0.055, color=(-0.7, -0.7, -0.7),
        bold=False, wrap=1.7):
    return visual.TextStim(win, text=text, pos=pos, height=height,
        color=color, bold=bold, wrapWidth=wrap,
        font="Helvetica", anchorHoriz="center", anchorVert="center")

def make_slider(pos, left_label, right_label):
    return visual.Slider(win,
        ticks=[1, 2, 3, 4, 5, 6, 7],
        labels=[left_label, "", "", "", "", "", right_label],
        pos=pos, size=(1.4, 0.07),
        style="rating", granularity=1,
        color=(-0.6, -0.6, -0.6),
        fillColor=(-0.1, -0.1, 0.6),
        borderColor=(-0.5, -0.5, -0.5),
        labelColor=(-0.5, -0.5, -0.5),
        labelHeight=0.042, font="Helvetica",
    )

def show_screen(stims):
    """Show a static screen and wait for SPACE."""
    cont = txt("Press SPACE to continue", pos=(0, -0.90),
               height=0.042, color=(-0.5, -0.5, -0.5))
    while True:
        for s in stims:
            s.draw()
        cont.draw()
        win.flip()
        keys = event.getKeys(["space", "escape"])
        if "escape" in keys:
            core.quit()
        if "space" in keys:
            return

# ---------------------------------------------------------------------------
# Passages and ground truth
# ---------------------------------------------------------------------------
PASSAGES = [
    {"id": "P01", "num": 1,  "drive": "press"},
    {"id": "P02", "num": 2,  "drive": "press"},
    {"id": "P03", "num": 3,  "drive": "press"},
    {"id": "P04", "num": 4,  "drive": "press"},
    {"id": "P05", "num": 5,  "drive": "wring"},
    {"id": "P06", "num": 6,  "drive": "press"},
    {"id": "P07", "num": 7,  "drive": "wring"},
    {"id": "P08", "num": 8,  "drive": "glide"},
    {"id": "P09", "num": 9,  "drive": "glide"},
    {"id": "P10", "num": 10, "drive": "slash"},
]

GROUND_TRUTH = {
    "P01": {"flow": 0.15, "intensity": 0.40, "space": 0.90},
    "P02": {"flow": 0.15, "intensity": 0.35, "space": 0.85},
    "P03": {"flow": 0.20, "intensity": 0.55, "space": 0.65},
    "P04": {"flow": 0.18, "intensity": 0.65, "space": 0.75},
    "P05": {"flow": 0.30, "intensity": 0.75, "space": 0.32},
    "P06": {"flow": 0.50, "intensity": 0.80, "space": 0.70},
    "P07": {"flow": 0.35, "intensity": 0.80, "space": 0.45},
    "P08": {"flow": 0.75, "intensity": 0.60, "space": 0.80},
    "P09": {"flow": 0.20, "intensity": 0.85, "space": 0.70},
    "P10": {"flow": 0.65, "intensity": 0.80, "space": 0.35},
}

EFFORT_SCALES = [
    ("weight", "Weight", "Light",    "Heavy"),
    ("time",   "Time",   "Sudden",   "Sustained"),
    ("space",  "Space",  "Indirect", "Direct"),
    ("flow",   "Flow",   "Free",     "Bound"),
]

EMOTION_SCALES = [
    ("valence", "Valence", "Unpleasant", "Pleasant"),
    ("arousal", "Arousal", "Calm",       "Activated"),
]

SCALES = EFFORT_SCALES + EMOTION_SCALES
SCALE_Y = [0.60, 0.36, 0.12, -0.12, -0.44, -0.68]

# ---------------------------------------------------------------------------
# Responses
# ---------------------------------------------------------------------------
rows = []

def record(pid, p_id, drive, scale_key, value):
    gt = GROUND_TRUTH.get(p_id, {})
    rows.append({
        "participant":        exp_info["Participant"],
        "session":            exp_info["Session"],
        "passage_num":        pid,
        "passage_id":         p_id,
        "drive":              drive,
        "scale":              scale_key,
        "participant_rating": value,
        "gt_flow":            gt.get("flow", ""),
        "gt_intensity":       gt.get("intensity", ""),
        "gt_space":           gt.get("space", ""),
    })

# ---------------------------------------------------------------------------
# Welcome screens (static -- created once)
# ---------------------------------------------------------------------------
show_screen([
    txt("Metamorphic Efforts", pos=(0, 0.75), height=0.080,
        color=(-0.85, -0.85, -0.85), bold=True),
    txt("Post-experience questionnaire", pos=(0, 0.60), height=0.050),
    txt(
        "You have just experienced the full piece.\n\n"
        "Now rate each of the ten sections based on your overall\n"
        "embodied experience -- the combined impression of text, voice,\n"
        "sound, and image working together.\n\n"
        "Rate the movement quality using four scales (Weight, Time, Space, Flow),\n"
        "and rate your emotional response using two scales (Valence, Arousal).\n\n"
        "There are no right or wrong answers.\n"
        "Respond based on what you remember feeling and perceiving.",
        pos=(0, 0.05), height=0.038, wrap=1.65
    ),
])

show_screen([
    txt("How to respond", pos=(0, 0.65), height=0.066,
        color=(-0.85, -0.85, -0.85), bold=True),
    txt(
        "Rate all six scales:\n"
        "  - Weight: from Light to Heavy\n"
        "  - Time: from Sudden to Sustained\n"
        "  - Space: from Indirect to Direct\n"
        "  - Flow: from Free to Bound\n"
        "  - Valence: from Unpleasant to Pleasant\n"
        "  - Arousal: from Calm to Activated\n\n"
        "Click to place your rating, then press SPACE to continue.",
        pos=(0, 0.0), height=0.036, wrap=1.55
    ),
])

# ---------------------------------------------------------------------------
# Pre-build all sliders for all passages (avoids per-frame creation)
# ---------------------------------------------------------------------------
all_passage_sliders = []
for passage in PASSAGES:
    passage_sliders = []
    for i, (key, name, left, right) in enumerate(SCALES):
        y = SCALE_Y[i]
        slider = make_slider(pos=(0, y), left_label=left, right_label=right)
        label = visual.TextStim(win, text=name, pos=(0, y + 0.070),
            height=0.028, color=(-0.5, -0.5, -0.5), bold=True,
            font="Helvetica", anchorHoriz="center", anchorVert="center")
        passage_sliders.append((key, slider, label))
    all_passage_sliders.append(passage_sliders)

# ---------------------------------------------------------------------------
# Main loop
# ---------------------------------------------------------------------------
for p_idx, passage in enumerate(PASSAGES):
    pid   = passage["num"]
    p_id  = passage["id"]
    drive = passage["drive"]

    stim_title.text = "Passage {}".format(pid)
    sliders = all_passage_sliders[p_idx]

    # Position dividers between each pair of scales
    for d_idx, div in enumerate(dividers):
        div.pos = (0, SCALE_Y[d_idx + 1] + 0.12)

    while True:
        stim_title.draw()
        stim_instr.draw()

        for d_idx, div in enumerate(dividers):
            div.draw()

        stim_emotion_label.draw()

        for key, slider, label in sliders:
            label.draw()
            slider.draw()

        all_rated = all(s.getRating() is not None for _, s, _ in sliders)
        if all_rated:
            stim_cont.draw()
        else:
            stim_warn.draw()

        win.flip()

        keys = event.getKeys(["space", "escape"])
        if "escape" in keys:
            core.quit()
        if "space" in keys and all_rated:
            break

    for key, slider, label in sliders:
        record(pid, p_id, drive, key, slider.getRating())

# ---------------------------------------------------------------------------
# Save
# ---------------------------------------------------------------------------
fieldnames = [
    "participant", "session", "passage_num", "passage_id", "drive",
    "scale", "participant_rating", "gt_flow", "gt_intensity", "gt_space"
]
with open(outfile, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

# ---------------------------------------------------------------------------
# Thank you
# ---------------------------------------------------------------------------
thank_stims = [
    txt("Thank you.", pos=(0, 0.2), height=0.10,
        color=(-0.85, -0.85, -0.85), bold=True),
    txt("Your responses have been saved.", pos=(0, -0.05), height=0.055),
    txt("Press SPACE to close.", pos=(0, -0.55), height=0.045,
        color=(-0.5, -0.5, -0.5)),
]
while True:
    for s in thank_stims:
        s.draw()
    win.flip()
    if event.getKeys(["space", "escape"]):
        break

win.close()
core.quit()
