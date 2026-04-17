#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Metamorphic Efforts -- Test A: Text-based Effort perception + emotion
PsychoPy 2023.x

Part 1 of the lab study. Participants read each full passage and rate:
  - 4 LMA Effort factors (Weight, Time, Space, Flow) on semantic differentials
  - 2 emotion dimensions (valence, arousal) from de Meijer's framework

Tests whether the BESS annotation reflects naive reader perception of
Kafka's prose, and whether Effort qualities predict emotional responses
(the embodiment claim).
"""

from psychopy import visual, event, core, gui
import os, csv, datetime

# ---------------------------------------------------------------------------
# Participant dialog
# ---------------------------------------------------------------------------
exp_info = {"Participant": "", "Session": "001"}
dlg = gui.DlgFromDict(exp_info, title="Metamorphic Efforts -- Text",
                      order=["Participant", "Session"])
if not dlg.OK:
    core.quit()

timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
os.makedirs("data", exist_ok=True)
outfile = "data/ME_TextA_P{}_S{}_{}.csv".format(
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
# Passage texts and ground truth
# ---------------------------------------------------------------------------
PASSAGE_TEXTS = {1: 'One morning, when Gregor Samsa woke from troubled dreams, he found himself transformed in his bed into a horrible vermin. He lay on his armour-like back, and if he lifted his head a little he could see his brown belly, slightly domed and divided by arches into stiff sections. The bedding was hardly able to cover it and seemed ready to slide off any moment. His many legs, pitifully thin compared with the size of the rest of him, waved about helplessly as he looked.', 2: '"What\'s happened to me?" he thought. It wasn\'t a dream. His room, a proper human room although a little too small, lay peacefully between its four familiar walls. A collection of textile samples lay spread out on the table and above it there hung a picture that he had recently cut out of an illustrated magazine and housed in a nice, gilded frame.\n\nGregor then turned to look out the window at the dull weather. Drops of rain could be heard hitting the pane, which made him feel quite sad.', 3: '"How about if I sleep a little bit longer and forget all this nonsense," he thought, but that was something he was unable to do because he was used to sleeping on his right, and in his present state couldn\'t get into that position. However hard he threw himself onto his right, he always rolled back to where he was.\n\n"Oh, God," he thought, "what a strenuous career it is that I\'ve chosen! Travelling day in and day out. It can all go to Hell!" He felt a slight itch up on his belly; pushed himself slowly up on his back towards the headboard so that he could lift his head better; found where the itch was, and saw that it was covered with lots of little white spots which he didn\'t know what to make of; and when he tried to feel the place with one of his legs he drew it quickly back because as soon as he touched it he was overcome by a cold shudder.', 4: 'And he looked over at the alarm clock, ticking on the chest of drawers. "God in Heaven!" he thought. It was half past six and the hands were quietly moving forwards, it was even later than half past, more like quarter to seven. Had the alarm clock not rung?\n\nHe was still hurriedly thinking all this through, unable to decide to get out of the bed, when the clock struck quarter to seven. There was a cautious knock at the door near his head. "Gregor," somebody called. It was his mother. "It\'s quarter to seven. Didn\'t you want to go somewhere?"', 5: 'Gregor was shocked when he heard his own voice answering, it could hardly be recognised as the voice he had had before. As if from deep inside him, there was a painful and uncontrollable squeaking mixed in with it, the words could be made out at first but then there was a sort of echo which made them unclear, leaving the hearer unsure whether he had heard properly or not.\n\nGregor had wanted to give a full answer and explain everything, but in the circumstances contented himself with saying: "Yes, mother, yes, thank-you, I\'m getting up now."', 6: 'It was a simple matter to throw off the covers; he only had to blow himself up a little and they fell off by themselves. But it became difficult after that, especially as he was so exceptionally broad. He would have used his arms and his hands to push himself up; but instead of them he only had all those little legs continuously moving in different directions, and which he was moreover unable to control.\n\nThe first thing he wanted to do was get the lower part of his body out of the bed, but he had never seen this lower part, and could not imagine what it looked like; it turned out to be too hard to move; it went so slowly; and finally, almost in a frenzy, when he carelessly shoved himself forwards with all the force he could gather, he chose the wrong direction, hit hard against the lower bedpost, and learned from the burning pain he felt that the lower part of his body might well, at present, be the most sensitive.', 7: 'The chief clerk now raised his voice. "Mr. Samsa, what is wrong? You barricade yourself in your room, give us no more than yes or no for an answer, you are causing serious and unnecessary concern to your parents and you fail to carry out your business duties in a way that is quite unheard of. I\'m speaking here on behalf of your parents and of your employer, and really must request a clear and immediate explanation."\n\n"But Sir," called Gregor, beside himself and forgetting all else in the excitement, "I\'ll open up immediately, just a moment. I\'m slightly unwell, an attack of dizziness, I haven\'t been able to get up. I\'m still in bed now."', 8: 'Gregor slowly pushed his way over to the door with the chair. Once there he let go of it and threw himself onto the door, holding himself upright against it using the adhesive on the tips of his legs. He rested there a little while to recover from the effort involved and then set himself to the task of turning the key in the lock with his mouth.\n\nUsing the jaw, he really was able to start the key turning, ignoring the fact that he must have been causing some kind of damage as a brown fluid came from his mouth, flowed over the key and dripped onto the floor.', 9: "Because he had to open the door in this way, it was already wide open before he could be seen. He had first to slowly turn himself around one of the double doors, and he had to do it very carefully if he did not want to fall flat on his back before entering the room.\n\nNow he also saw the chief clerk, his hand pressed against his open mouth and slowly retreating as if driven by a steady and invisible force. Gregor's mother sank down onto the floor. His father clenched his fists as if wanting to knock Gregor back into his room. Then he looked uncertainly round the living room, covered his eyes with his hands and wept so that his powerful chest shook.", 10: "Gregor's father seized the chief clerk's stick in his right hand, picked up a large newspaper from the table with his left, and used them to drive Gregor back into his room, stamping his foot at him as he went. Nothing would stop Gregor's father as he drove him back, making hissing noises at him like a wild man.\n\nGregor pushed himself into the doorway without regard for what might happen. One side of his body lifted itself, he lay at an angle in the doorway, one flank scraped on the white door and was painfully injured, leaving vile brown flecks on it. Soon he was stuck fast and would not have been able to move at all by himself. Then his father gave him a hefty shove from behind which released him from where he was held and sent him flying, and heavily bleeding, deep into his room. The door was slammed shut with the stick, then, finally, all was quiet."}

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
    ("weight", "Light",    "Heavy"),
    ("time",   "Sudden",   "Sustained"),
    ("space",  "Indirect", "Direct"),
    ("flow",   "Free",     "Bound"),
]

EMOTION_SCALES = [
    ("valence", "Unpleasant", "Pleasant"),
    ("arousal", "Calm",       "Activated"),
]

SCALES = EFFORT_SCALES + EMOTION_SCALES
SCALE_Y = [0.10, -0.06, -0.22, -0.38, -0.60, -0.76]

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def txt(text, pos=(0, 0), height=0.048, color=(-0.7, -0.7, -0.7),
        bold=False, wrap=1.7, font="Helvetica", italic=False):
    return visual.TextStim(
        win, text=text, pos=pos, height=height,
        color=color, bold=bold, wrapWidth=wrap,
        font=font, italic=italic,
        anchorHoriz="center", anchorVert="center"
    )

def make_slider(pos, left_label, right_label):
    return visual.Slider(
        win, ticks=[1, 2, 3, 4, 5, 6, 7],
        labels=[left_label, "", "", "", "", "", right_label],
        pos=pos, size=(1.0, 0.05),
        style="rating", granularity=1,
        color=(-0.6, -0.6, -0.6),
        fillColor=(-0.1, -0.1, 0.6),
        borderColor=(-0.5, -0.5, -0.5),
        labelColor=(-0.5, -0.5, -0.5),
        labelHeight=0.036, font="Helvetica",
    )

def show_screen(stims):
    cont = txt("Press SPACE to continue", pos=(0, -0.92),
               height=0.038, color=(-0.5, -0.5, -0.5))
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
# Reusable stims
# ---------------------------------------------------------------------------
stim_header = visual.TextStim(win, text="", pos=(0, 0.90), height=0.052,
    color=(-0.85, -0.85, -0.85), bold=True, wrapWidth=1.7,
    font="Helvetica", anchorHoriz="center", anchorVert="center")

stim_passage = visual.TextStim(win, text="", pos=(0, 0.55), height=0.040,
    color=(-0.2, -0.2, -0.2), wrapWidth=1.7,
    font="Georgia", anchorHoriz="center", anchorVert="center")

stim_instr = visual.TextStim(win,
    text="Rate the movement quality and your emotional response.",
    pos=(0, 0.18), height=0.034, color=(-0.6, -0.6, -0.6),
    wrapWidth=1.6, font="Helvetica",
    anchorHoriz="center", anchorVert="center")

stim_emotion_label = visual.TextStim(win, text="Your emotional response:",
    pos=(0, -0.49), height=0.028, color=(-0.4, -0.4, -0.4),
    italic=True, font="Helvetica",
    anchorHoriz="center", anchorVert="center")

stim_cont = visual.TextStim(win, text="Press SPACE to continue",
    pos=(0, -0.92), height=0.038, color=(-0.5, -0.5, -0.5),
    font="Helvetica", anchorHoriz="center", anchorVert="center")

stim_warn = visual.TextStim(win, text="Rate all six scales before continuing.",
    pos=(0, -0.92), height=0.038, color=(0.5, -0.3, -0.3),
    font="Helvetica", anchorHoriz="center", anchorVert="center")

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
# Welcome and instructions
# ---------------------------------------------------------------------------
show_screen([
    txt("Metamorphic Efforts", pos=(0, 0.65), height=0.080,
        color=(-0.85, -0.85, -0.85), bold=True),
    txt("Text perception questionnaire", pos=(0, 0.47), height=0.050),
    txt(
        "You will read ten passages from Kafka's The Metamorphosis.\n\n"
        "After reading each passage, rate the movement quality you perceive\n"
        "using four scales, and rate your emotional response\n"
        "using two additional scales.\n\n"
        "There are no right or wrong answers.\n"
        "Respond based on your immediate impression.",
        pos=(0, 0.02), height=0.044, wrap=1.55
    ),
])

show_screen([
    txt("How to respond", pos=(0, 0.65), height=0.066,
        color=(-0.85, -0.85, -0.85), bold=True),
    txt(
        "Read the passage carefully. You may re-read it as many times as you like.\n\n"
        "Then rate all six scales. Each scale runs between two opposite qualities.\n\n"
        "Click to place your rating, then press SPACE to continue.",
        pos=(0, 0.05), height=0.044, wrap=1.55
    ),
])

# ---------------------------------------------------------------------------
# Pre-build sliders and dividers
# ---------------------------------------------------------------------------
scale_dividers = []
for i in range(1, 6):
    scale_dividers.append(visual.TextStim(win, text="-" * 50, pos=(0, 0),
        height=0.012, color=(-0.80, -0.80, -0.80),
        font="Helvetica", anchorHoriz="center", anchorVert="center"))

all_passage_sliders = []
for passage in PASSAGES:
    passage_sliders = []
    for i, (key, left, right) in enumerate(SCALES):
        y = SCALE_Y[i]
        slider = make_slider(pos=(0, y), left_label=left, right_label=right)
        passage_sliders.append((key, slider))
    all_passage_sliders.append(passage_sliders)

# Passage text divider (between text and scales)
stim_text_divider = visual.TextStim(win, text="-" * 70, pos=(0, 0.22),
    height=0.012, color=(-0.78, -0.78, -0.78),
    font="Helvetica", anchorHoriz="center", anchorVert="center")

# ---------------------------------------------------------------------------
# Main loop
# ---------------------------------------------------------------------------
for p_idx, passage in enumerate(PASSAGES):
    pid   = passage["num"]
    p_id  = passage["id"]
    drive = passage["drive"]

    stim_header.text = "Passage {}".format(pid)
    stim_passage.text = PASSAGE_TEXTS.get(pid, "")
    sliders = all_passage_sliders[p_idx]

    # Position dividers between each pair of scales
    for d_idx, div in enumerate(scale_dividers):
        div.pos = (0, SCALE_Y[d_idx + 1] + 0.09)

    while True:
        stim_header.draw()
        stim_passage.draw()
        stim_text_divider.draw()
        stim_instr.draw()

        for d_idx, div in enumerate(scale_dividers):
            div.draw()

        stim_emotion_label.draw()

        for key, slider in sliders:
            slider.draw()

        all_rated = all(s.getRating() is not None for _, s in sliders)
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

    for key, slider in sliders:
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
    txt("Thank you.", pos=(0, 0.2), height=0.09,
        color=(-0.85, -0.85, -0.85), bold=True),
    txt("Your responses have been saved.", pos=(0, -0.05), height=0.048),
    txt("Press SPACE to close.", pos=(0, -0.55), height=0.040,
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
