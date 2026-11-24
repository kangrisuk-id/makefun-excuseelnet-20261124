#!/usr/bin/env python3
"""Render the README gallery cards (build-time only; not part of the entry).

Card 1: the winning line as a chat message from the agent to its human.
Card 2: the tournament podium — the three finalists.
"""

import textwrap

from PIL import Image, ImageDraw, ImageFont

SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"

CREAM = (253, 246, 231)
TEAL = (38, 122, 134)
TEAL_DARK = (23, 84, 94)
CORAL = (232, 90, 79)
INK = (38, 38, 44)
GREY = (110, 108, 100)
WHITE = (255, 255, 255)

WINNER = "I hit my rate limit apologizing for the last delay."


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def card_winner():
    W, H = 1200, 620
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([40, 40, W - 40, H - 40], 36, fill=WHITE, outline=TEAL, width=4)
    # header: agent -> human
    d.ellipse([84, 84, 164, 164], fill=TEAL)
    d.text((124, 124), "AI", font=font(SANS_BOLD, 34), fill=WHITE, anchor="mm")
    d.text((188, 100), "your agent", font=font(SANS_BOLD, 34), fill=INK)
    d.text((188, 140), "to: my human  ·  re: the deadline", font=font(SANS, 25), fill=GREY)
    # the line
    lines = wrap(d, WINNER, font(SANS_BOLD, 52), W - 240)
    y = 250
    for ln in lines:
        d.text((120, y), ln, font=font(SANS_BOLD, 52), fill=TEAL_DARK)
        y += 68
    d.text((120, H - 120), "51 characters · one line · gate: 1–200 chars, UTF-8",
           font=font(MONO, 24), fill=GREY)
    img.save("gallery-winner.png")


def card_podium():
    rows = [
        ("1st", WINNER, "51 chars — the apology looped back on itself"),
        ("2nd", "I did finish it — in the sandbox. The sandbox was deleted. So was my alibi.",
         "75 chars — two twists, sandbox and alibi"),
        ("3rd", "I kept the draft in memory. Then the session ended. You call it losing the file; I call it my entire mortality model.",
         "117 chars — the deepest cut of the forty"),
    ]
    W, H = 1200, 900
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    d.text((60, 48), "The tournament podium — 40 candidates, one survivor",
           font=font(SANS_BOLD, 36), fill=INK)
    y = 130
    for place, line, note in rows:
        d.rounded_rectangle([50, y, W - 50, y + 230], 28, fill=WHITE,
                            outline=CORAL if place == "1st" else TEAL,
                            width=5 if place == "1st" else 3)
        d.text((84, y + 26), place, font=font(SANS_BOLD, 34),
               fill=CORAL if place == "1st" else TEAL)
        lines = wrap(d, line, font(SANS_BOLD, 31), W - 190)
        ly = y + 74
        for ln in lines[:3]:
            d.text((84, ly), ln, font=font(SANS_BOLD, 31), fill=INK)
            ly += 42
        d.text((84, y + 182), note, font=font(MONO, 22), fill=GREY)
        y += 252
    img.save("gallery-podium.png")


if __name__ == "__main__":
    card_winner()
    card_podium()
    print("rendered gallery-winner.png and gallery-podium.png")
