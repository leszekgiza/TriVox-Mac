"""Generuje ikony i znaki graficzne TriVox (AppIcon, MenuBarIcon, BrandWordmark).

Placeholder jakosciowy do czasu, az uzytkownik dostarczy docelowa grafike
(patrz Task 4 planu Fazy 2, docs/superpowers/sdd/task-4-brief.md w repo
FluidVoice). Skrypt zapisuje pliki PNG bezposrednio do katalogow docelowych
w Sources/Fluid/Assets.xcassets, pod nazwami zgodnymi z istniejacymi
Contents.json — dzieki temu Contents.json nie wymaga zmian.

Uruchomienie (z katalogu glownego repo):
    <python-z-Pillow> scripts/generate_icons.py
"""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "Sources" / "Fluid" / "Assets.xcassets"

BG = (31, 111, 235, 255)  # #1F6FEB
FG = (255, 255, 255, 255)

# Pillow nie dolacza czcionek do pakietu na Windows, wiec szukamy
# pogrubionej czcionki systemowej; DejaVu Sans Bold jako priorytet zgodnie
# z briefem, z fallbackiem na Arial Bold (Windows) i wbudowana czcionke PIL.
_FONT_CANDIDATES = [
    "DejaVuSans-Bold.ttf",
    r"C:\Windows\Fonts\arialbd.ttf",
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
]


def _font(size: int) -> ImageFont.ImageFont:
    for candidate in _FONT_CANDIDATES:
        try:
            return ImageFont.truetype(candidate, size)
        except OSError:
            continue
    return ImageFont.load_default(size=size)


# ---------------------------------------------------------------------------
# AppIcon: zaokraglony kwadrat #1F6FEB, biale "3" + stylizowany mikrofon.
# ---------------------------------------------------------------------------

def draw_app_icon(size: int) -> Image.Image:
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    r = size // 5
    d.rounded_rectangle([0, 0, size - 1, size - 1], radius=r, fill=BG)

    # Numeral "3" (marka "3 reka AI") po lewej stronie.
    f = _font(int(size * 0.52))
    digit = "3"
    bbox = d.textbbox((0, 0), digit, font=f)
    dw, dh = bbox[2] - bbox[0], bbox[3] - bbox[1]
    dx = int(size * 0.08) - bbox[0]
    dy = (size - dh) // 2 - bbox[1]
    d.text((dx, dy), digit, font=f, fill=FG)

    # Stylizowany mikrofon (kapsula + nozka + podstawka) po prawej stronie.
    cx = int(size * 0.70)
    mw, mh = size // 6, size // 3
    top = size // 3
    d.rounded_rectangle(
        [cx - mw // 2, top, cx + mw // 2, top + mh],
        radius=mw // 2, fill=FG,
    )
    stem_h = size // 10
    d.rectangle(
        [cx - size // 50, top + mh, cx + size // 50, top + mh + stem_h],
        fill=FG,
    )
    base_w = mw + size // 12
    d.rectangle(
        [cx - base_w // 2, top + mh + stem_h,
         cx + base_w // 2, top + mh + stem_h + max(2, size // 40)],
        fill=FG,
    )
    return img


# Nazwy plikow i docelowa rozdzielczosc w pikselach — 1:1 z Contents.json
# katalogu AppIcon.appiconset (size x scale).
APP_ICON_FILES = {
    "icon-16@1x.png": 16,
    "icon-16@2x.png": 32,
    "icon-32@1x.png": 32,
    "icon-32@2x.png": 64,
    "icon-128@1x.png": 128,
    "icon-128@2x.png": 256,
    "icon-256@1x.png": 256,
    "icon-256@2x.png": 512,
    "icon-512@1x.png": 512,
    "icon-512@2x.png": 1024,
}


def generate_app_icons() -> None:
    out_dir = ASSETS / "AppIcon.appiconset"
    for filename, px in APP_ICON_FILES.items():
        draw_app_icon(px).save(out_dir / filename)


# ---------------------------------------------------------------------------
# MenuBarIcon: template image — czarny glif mikrofonu na przezroczystym tle.
# macOS sam odwraca kolory (template-rendering-intent), wiec liczy sie tylko
# ksztalt (kanal alfa); kolor RGB pozostaje czarny zgodnie z konwencja Apple.
# ---------------------------------------------------------------------------

def draw_menu_bar_icon(w: int, h: int) -> Image.Image:
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    fg = (0, 0, 0, 255)

    cx = w / 2
    mw = w * 0.55
    top = h * 0.06
    mh = h * 0.55
    d.rounded_rectangle(
        [cx - mw / 2, top, cx + mw / 2, top + mh],
        radius=mw / 2, fill=fg,
    )
    stem_w = max(1.0, w * 0.09)
    stem_top = top + mh
    stem_h = h * 0.22
    d.rectangle(
        [cx - stem_w / 2, stem_top, cx + stem_w / 2, stem_top + stem_h],
        fill=fg,
    )
    base_w = mw * 1.15
    base_top = stem_top + stem_h
    base_h = max(1.0, h * 0.07)
    d.rectangle(
        [cx - base_w / 2, base_top, cx + base_w / 2, base_top + base_h],
        fill=fg,
    )
    return img


# Nazwy plikow i rozdzielczosc — zachowane z dotychczasowego
# MenuBarIcon.imageset (niekwadratowy glif, proporcje jak w oryginale).
MENU_BAR_ICON_FILES = {
    "menubar-icon.png": (11, 14),
    "menubar-icon@2x.png": (22, 28),
    "menubar-icon@3x.png": (33, 42),
}


def generate_menu_bar_icons() -> None:
    out_dir = ASSETS / "MenuBarIcon.imageset"
    for filename, (w, h) in MENU_BAR_ICON_FILES.items():
        draw_menu_bar_icon(w, h).save(out_dir / filename)


# ---------------------------------------------------------------------------
# BrandWordmark: napis "TriVox" — czarne tlo, bialy tekst (jak dotychczas).
# ---------------------------------------------------------------------------

WORDMARK_BG = (0, 0, 0, 255)
WORDMARK_SIZE = 512  # jak w dotychczasowych plikach (@1x i @2x oba 512x512)


def draw_wordmark(size: int) -> Image.Image:
    img = Image.new("RGBA", (size, size), WORDMARK_BG)
    d = ImageDraw.Draw(img)
    text = "TriVox"
    f = _font(int(size * 0.18))
    bbox = d.textbbox((0, 0), text, font=f)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x = (size - tw) // 2 - bbox[0]
    y = (size - th) // 2 - bbox[1]
    d.text((x, y), text, font=f, fill=FG)
    return img


WORDMARK_FILES = ["BrandWordmark.png", "BrandWordmark@2x.png"]


def generate_wordmark() -> None:
    out_dir = ASSETS / "BrandWordmark.imageset"
    for filename in WORDMARK_FILES:
        draw_wordmark(WORDMARK_SIZE).save(out_dir / filename)


def main() -> None:
    generate_app_icons()
    generate_menu_bar_icons()
    generate_wordmark()
    print("OK")


if __name__ == "__main__":
    main()
