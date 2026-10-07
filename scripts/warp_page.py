"""Paste a real page onto a quad in a frame (perspective warp, 4x supersampled).
usage: python3 scripts/warp_page.py frame.png page.png out.png x0,y0 x1,y1 x2,y2 x3,y3 [shade]
corners: TL TR BR BL in frame pixels. shade: brightness multiplier (default 0.92)."""
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

frame_p, page_p, out_p = sys.argv[1:4]
quad = [tuple(map(float, c.split(","))) for c in sys.argv[4:8]]
shade = float(sys.argv[8]) if len(sys.argv) > 8 else 0.92
S = 4
frame = Image.open(frame_p).convert("RGB")
page = Image.open(page_p).convert("RGB")
W, H = frame.size
pw, ph = page.size
dst = [(x * S, y * S) for x, y in quad]
src = [(0, 0), (pw, 0), (pw, ph), (0, ph)]
# coefficients mapping output (dst) -> input (src)
A, b = [], []
for (x, y), (u, v) in zip(dst, src):
    A += [[x, y, 1, 0, 0, 0, -u * x, -u * y], [0, 0, 0, x, y, 1, -v * x, -v * y]]
    b += [u, v]
coef = np.linalg.solve(np.array(A), np.array(b))
big = page.transform((W * S, H * S), Image.PERSPECTIVE, tuple(coef), Image.BICUBIC)
mask = Image.new("L", (W * S, H * S), 0)
ImageDraw.Draw(mask).polygon(dst, fill=255)
warped = big.resize((W, H), Image.LANCZOS)
mask = mask.resize((W, H), Image.LANCZOS).filter(ImageFilter.GaussianBlur(0.6))
# light falloff: brighter toward top-right (key light), darker toward bottom-left
gx, gy = np.meshgrid(np.linspace(0, 1, W), np.linspace(0, 1, H))
light = shade * (1.0 + 0.10 * (gx - 0.5) - 0.12 * (gy - 0.6))
arr = np.clip(np.asarray(warped, dtype=np.float32) * light[..., None], 0, 255).astype(np.uint8)
out = frame.copy()
out.paste(Image.fromarray(arr), (0, 0), mask)
out.save(out_p)
print("saved", out_p)
