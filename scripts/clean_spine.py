"""Paint a plain dark spine band (no invented text). usage: in.png out.png x,y x,y x,y x,y"""
import sys
from PIL import Image, ImageDraw, ImageFilter
im = Image.open(sys.argv[1]).convert("RGB")
poly = [tuple(map(float, p.split(","))) for p in sys.argv[3:]]
S = 4
mask = Image.new("L", (im.width * S, im.height * S), 0)
ImageDraw.Draw(mask).polygon([(x * S, y * S) for x, y in poly], fill=255)
mask = mask.resize(im.size, Image.LANCZOS).filter(ImageFilter.GaussianBlur(0.7))
band = Image.new("RGB", im.size, (20, 22, 32))
im.paste(band, (0, 0), mask)
im.save(sys.argv[2]); print("saved", sys.argv[2])
