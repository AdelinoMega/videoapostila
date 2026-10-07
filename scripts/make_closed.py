"""Build a 'closed workbook' frame from base_A: replace the left page with desk texture taken
from the same photo (rows below the book, perspective-scaled, luminance matched to the desk
strip left of the book), then the real cover is composited onto the right-page quad."""
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
base = Image.open("output/frames/base_A.png").convert("RGB")
a = np.asarray(base, dtype=np.float32)
H, W, _ = a.shape
fill = a.copy()
strip = a[:, 2:62]                       # real desk immediately left of the book
tile = np.concatenate([strip, strip[:, ::-1]], axis=1)
reps = W // tile.shape[1] + 1
row_tiled = np.tile(tile, (1, reps, 1))[:, :W]
# shift each 120px block vertically by a few rows so the mirror seams are less regular
for i, x in enumerate(range(0, W, 120)):
    row_tiled[:, x:x + 120] = np.roll(row_tiled[:, x:x + 120], (i * 7) % 23, axis=0)
fill = np.asarray(Image.fromarray(row_tiled.astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.2)), dtype=np.float32)
poly = [(85, 596), (340, 604), (368, 640), (368, 1092), (30, 1092), (40, 1000)]
S = 4
m = Image.new("L", (W * S, H * S), 0)
ImageDraw.Draw(m).polygon([(x * S, y * S) for x, y in poly], fill=255)
mask = np.asarray(m.resize((W, H), Image.LANCZOS).filter(ImageFilter.GaussianBlur(2)), dtype=np.float32)[..., None] / 255
out = a * (1 - mask) + fill * mask
# soft contact shadow along the closed book's spine (left edge of right page)
img = Image.fromarray(np.clip(out, 0, 255).astype(np.uint8))
sh = Image.new("L", (W, H), 0)
ImageDraw.Draw(sh).polygon([(350, 645), (360, 649), (360, 1060), (345, 1062)], fill=120)
sh = sh.filter(ImageFilter.GaussianBlur(5))
img = Image.composite(Image.new("RGB", (W, H), (20, 14, 10)), img, sh)
img.save("output/frames/base_closedA.png"); print("ok")
