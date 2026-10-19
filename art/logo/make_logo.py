"""Pixel-art "At Your Servus" sign with a Bavarian lozenge band, transparent background."""
import random
import sys
from pathlib import Path

from PIL import Image

GLYPHS = {
    "A": [".###.", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"],
    "T": ["#####", "..#..", "..#..", "..#..", "..#..", "..#..", "..#.."],
    "Y": ["#...#", "#...#", ".#.#.", "..#..", "..#..", "..#..", "..#.."],
    "O": [".###.", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."],
    "U": ["#...#", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."],
    "R": ["####.", "#...#", "#...#", "####.", "#.#..", "#..#.", "#...#"],
    "S": [".####", "#....", "#....", ".###.", "....#", "....#", "####."],
    "E": ["#####", "#....", "#....", "####.", "#....", "#....", "#####"],
    "V": ["#...#", "#...#", "#...#", "#...#", "#...#", ".#.#.", "..#.."],
    " ": ["...", "...", "...", "...", "...", "...", "..."],
}

WOOD = [(176, 132, 80), (164, 121, 72), (184, 140, 86), (156, 114, 68)]
SEAM = (104, 72, 40)
BORDER = (66, 44, 24)
BORDER_HI = (96, 66, 38)
NAIL = (60, 60, 66)
NAIL_HI = (150, 150, 160)
BLUE = (0, 140, 210)
BLUE_DARK = (0, 104, 168)
WHITE = (245, 248, 252)
CHAIN = (90, 90, 98)
CHAIN_HI = (160, 160, 170)
GOLD = (255, 214, 74)
GOLD_DARK = (224, 168, 40)
CREAM = (255, 246, 222)
CREAM_DARK = (236, 214, 170)
SHADOW = (52, 32, 16)


def text_width(text, scale):
    return sum((len(GLYPHS[c][0]) + 1) * scale for c in text) - scale


def draw_text(px, text, x0, y0, scale, top, bottom):
    x = x0
    for c in text:
        g = GLYPHS[c]
        for gy, row in enumerate(g):
            for gx, cell in enumerate(row):
                if cell != "#":
                    continue
                color = top if gy < 3 else bottom
                for dy in range(scale):
                    for dx in range(scale):
                        sx, sy = x + gx * scale + dx, y0 + gy * scale + dy
                        # Minecraft-style drop shadow, one scale step down-right
                        px[sx + 1, sy + 1] = SHADOW + (255,)
        x += (len(g[0]) + 1) * scale
    x = x0
    for c in text:
        g = GLYPHS[c]
        for gy, row in enumerate(g):
            for gx, cell in enumerate(row):
                if cell != "#":
                    continue
                color = top if gy < 3 else bottom
                for dy in range(scale):
                    for dx in range(scale):
                        px[x + gx * scale + dx, y0 + gy * scale + dy] = color + (255,)
        x += (len(g[0]) + 1) * scale


def build():
    rng = random.Random(7)
    big, small = 2, 1
    w = text_width("SERVUS", big) + 20
    chain_h, band_h = 8, 12
    board_top = chain_h
    board_h = 2 + band_h + 5 + 7 + 4 + 7 * big + 7 + 2
    h = board_top + board_h
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    px = img.load()

    # chains
    for cx in (12, w - 13):
        for y in range(chain_h):
            link = (y // 2) % 2
            px[cx, y] = (CHAIN_HI if link else CHAIN) + (255,)
            if not link:
                px[cx - 1, y] = CHAIN + (255,)
                px[cx + 1, y] = CHAIN + (255,)

    # board: horizontal planks with grain noise
    for y in range(board_h):
        plank = (y - 2) // 6
        for x in range(w):
            if (y - 2) % 6 == 5:
                c = SEAM
            else:
                c = WOOD[(rng.random() < 0.18) * rng.randrange(1, 4)]
                if rng.random() < 0.04:
                    c = WOOD[3]
            px[x, board_top + y] = c + (255,)
        # vertical joint, staggered per plank
        jx = 18 + (plank * 37) % (w - 36)
        if (y - 2) % 6 != 5:
            px[jx, board_top + y] = SEAM + (255,)

    # Bavarian lozenge band (diagonal diamonds)
    band_y = board_top + 2
    for y in range(band_h):
        for x in range(w):
            # a row of 12x12 blue diamonds with white ones in between
            yy = y + 6
            x_ = x + (12 - w % 12) // 2
            blue = ((x_ + yy) // 12 + (x_ - yy + 240) // 12) % 2 == 0
            shade = (x_ + yy) % 12 < 3 or (x_ - yy + 240) % 12 < 3
            c = (BLUE_DARK if shade else BLUE) if blue else WHITE
            px[x, band_y + y] = c + (255,)
    for x in range(w):
        px[x, band_y + band_h] = SEAM + (255,)

    # frame
    for x in range(w):
        for t in (0, 1):
            px[x, board_top + t] = (BORDER if t == 0 else BORDER_HI) + (255,)
            px[x, h - 1 - t] = (BORDER if t == 0 else BORDER_HI) + (255,)
    for y in range(board_top, h):
        for t in (0, 1):
            px[t, y] = (BORDER if t == 0 else BORDER_HI) + (255,)
            px[w - 1 - t, y] = (BORDER if t == 0 else BORDER_HI) + (255,)

    # nails where the chains hold the board
    for cx in (12, w - 13):
        px[cx, band_y + band_h + 2] = NAIL + (255,)
    for cx in (5, w - 6):
        ny = h - 6
        px[cx, ny] = NAIL + (255,)
        px[cx, ny - 1] = NAIL_HI + (255,)

    # text
    ty = band_y + band_h + 5
    draw_text(px, "AT YOUR", (w - text_width("AT YOUR", small)) // 2, ty, small, GOLD, GOLD_DARK)
    ty += 7 + 4
    draw_text(px, "SERVUS", (w - text_width("SERVUS", big)) // 2, ty, big, CREAM, CREAM_DARK)
    return img


SKY = [(92, 156, 230), (112, 172, 236), (134, 188, 242), (158, 204, 246), (182, 220, 250)]
ROCK = (122, 128, 150)
ROCK_DARK = (98, 104, 128)
SNOW = (240, 244, 250)
SNOW_SHADE = (206, 218, 236)
GRASS = [(96, 164, 64), (84, 150, 56), (108, 176, 72)]
GRASS_DARK = (66, 124, 44)
CLOUD = (250, 252, 255)


def ridge(peaks, x):
    """Height of a piecewise linear ridge through (x, y) peaks."""
    for (x0, y0), (x1, y1) in zip(peaks, peaks[1:]):
        if x0 <= x <= x1:
            return y0 + (y1 - y0) * (x - x0) / (x1 - x0)
    return peaks[-1][1]


def build_square(size=96):
    """The sign hanging in front of the Alps, square with an opaque background, for the CurseForge project logo."""
    rng = random.Random(11)
    sign = build()
    img = Image.new("RGBA", (size, size), (0, 0, 0, 255))
    px = img.load()
    sx, sy = (size - sign.width) // 2, size - sign.height - 11

    # sky in hard pixel bands, lighter towards the horizon
    for y in range(size):
        band = SKY[min(len(SKY) - 1, y * len(SKY) // (sy + 30))]
        for x in range(size):
            px[x, y] = band + (255,)
    for cx, cy, cw in ((8, 6, 9), (70, 3, 12)):
        for dx in range(cw):
            px[cx + dx, cy + 1] = CLOUD + (255,)
            if 2 <= dx < cw - 2:
                px[cx + dx, cy] = CLOUD + (255,)

    # far mountains with snow caps, peaking above the sign
    peaks = [(0, 30), (10, 16), (22, 26), (34, 9), (48, 24), (60, 12), (74, 22), (86, 7), (96, 20)]
    for x in range(size):
        top = int(ridge(peaks, x))
        for y in range(top, size):
            depth = y - top
            left_face = ridge(peaks, x + 1) < ridge(peaks, x)  # slope rising to the right is in shadow
            if depth < 5 and top < 20:
                c = SNOW_SHADE if left_face else SNOW
            else:
                c = ROCK_DARK if left_face else ROCK
            px[x, y] = c + (255,)

    # meadow
    hills = [(0, size - 16), (24, size - 19), (52, size - 14), (78, size - 18), (96, size - 15)]
    for x in range(size):
        top = int(ridge(hills, x))
        for y in range(top, size):
            c = GRASS_DARK if y == top else GRASS[(rng.random() < 0.25) * rng.randrange(1, 3)]
            px[x, y] = c + (255,)

    # chains from the top edge down to the sign's own chains
    for cx in (sx + 12, sx + sign.width - 13):
        for y in range(sy):
            link = (y // 2) % 2
            px[cx, y] = (CHAIN_HI if link else CHAIN) + (255,)
            if not link:
                px[cx - 1, y] = CHAIN + (255,)
                px[cx + 1, y] = CHAIN + (255,)
    img.alpha_composite(sign, (sx, sy))
    return img.convert("RGB")


if __name__ == "__main__":
    out = Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=True)
    base = build()
    base.save(out / "at-your-servus-1x.png")
    for s in (8, 16):
        base.resize((base.width * s, base.height * s), Image.NEAREST).save(out / f"at-your-servus-{s}x.png")
    square = build_square()
    square.save(out / "at-your-servus-square-1x.png")
    square.resize((square.width * 8, square.height * 8), Image.NEAREST).save(out / "at-your-servus-square-8x.png")
    print(base.size, square.size)
