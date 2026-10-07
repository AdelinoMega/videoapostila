import sys; sys.path.insert(0, "scripts")
from runway import run, data_uri
prompt = ("Exactly the same photo as @scene: same camera, same desk, same MacBook, same headphones, same lighting. "
  "The only change: the printed A4 workbook is now CLOSED, so it is only HALF as wide as the open book: a tall portrait "
  "rectangle, taller than it is wide, lying on the right half of the desk exactly over the area of the former right-hand page, "
  "its left edge (the spine) on the vertical center line of the frame, its right edge where the right page ended. The left half of "
  "the desk in front of the laptop is empty wood. The front cover is "
  "plain dark navy blue with nothing printed on it, matte, realistic thickness with white page edges visible at the bottom and right. "
  "Where the left-hand page was there is now only the bare wooden desk. No people, no hands, no text, no watermark.")
run("/v1/text_to_image", {"model": "gen4_image", "ratio": "720:1280", "seed": 1204, "promptText": prompt,
  "referenceImages": [{"uri": data_uri("output/frames/base_A.jpg"), "tag": "scene"}]}, "output/frames/base_closed2.png")
