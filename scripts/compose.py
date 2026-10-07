"""Compose real workbook pages onto a generated base frame.
Shading (gutter shadow, paper curvature, light falloff) is transferred from the blank
page in the base frame onto the real page, so no page content is invented.

usage: python3 scripts/compose.py base.png out.png [--zoom Z cx cy] [--shade-from-base] PAGE QUAD [PAGE QUAD ...]
  QUAD = "x,y x,y x,y x,y"  (TL TR BR BL, in base-frame pixels before zoom)
"""
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

S = 4


def solve(dst, src):
    A, b = [], []
    for (x, y), (u, v) in zip(dst, src):
        A += [[x, y, 1, 0, 0, 0, -u * x, -u * y], [0, 0, 0, x, y, 1, -v * x, -v * y]]
        b += [u, v]
    return tuple(np.linalg.solve(np.array(A), np.array(b)))


def main(argv):
    base_p, out_p, rest = argv[0], argv[1], argv[2:]
    zoom, shade_base = None, False
    while rest and rest[0].startswith("--"):
        if rest[0] == "--zoom":
            zoom = tuple(map(float, rest[1:4])); rest = rest[4:]
        elif rest[0] == "--shade-from-base":
            shade_base = True; rest = rest[1:]
    base = Image.open(base_p).convert("RGB")
    W, H = base.size
    T = lambda p: p
    if zoom:
        z, cx, cy = zoom
        cw, ch = W / z, H / z
        x0 = min(max(cx - cw / 2, 0), W - cw); y0 = min(max(cy - ch / 2, 0), H - ch)
        base = base.crop((round(x0), round(y0), round(x0 + cw), round(y0 + ch))).resize((W, H), Image.LANCZOS)
        T = lambda p: ((p[0] - x0) * z, (p[1] - y0) * z)
    out = base.copy()
    lum = np.asarray(base.convert("L"), dtype=np.float32)
    for page_p, quad_s in zip(rest[0::2], rest[1::2]):
        quad = [T(tuple(map(float, c.split(",")))) for c in quad_s.split()]
        page = Image.open(page_p).convert("RGB")
        pw, ph = page.size
        dst = [(x * S, y * S) for x, y in quad]
        coef = solve(dst, [(0, 0), (pw, 0), (pw, ph), (0, ph)])
        warped = page.transform((W * S, H * S), Image.PERSPECTIVE, coef, Image.BICUBIC).resize((W, H), Image.LANCZOS)
        m = Image.new("L", (W * S, H * S), 0)
        ImageDraw.Draw(m).polygon(dst, fill=255)
        mask = m.resize((W, H), Image.LANCZOS).filter(ImageFilter.GaussianBlur(0.6))
        mk = np.asarray(mask) > 200
        if shade_base:
            ref = np.percentile(lum[mk], 97)
            light = np.clip(lum / ref, 0.35, 1.0)
            light = np.asarray(Image.fromarray((light * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(3)), dtype=np.float32) / 255
            light = 0.95 * light
        else:
            light = np.full((H, W), 0.92, dtype=np.float32)
        arr = np.clip(np.asarray(warped, dtype=np.float32) * light[..., None], 0, 255).astype(np.uint8)
        out.paste(Image.fromarray(arr), (0, 0), mask)
    out.save(out_p)
    print("saved", out_p)


main(sys.argv[1:])
