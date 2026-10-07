import sys; sys.path.insert(0, "scripts")
from runway import run, data_uri
which = sys.argv[1]
common = ("Photorealistic cinematic product photo, vertical. Exactly the same desk, wooden surface, warm soft key light, "
          "dark background with subtle blue and orange bokeh, same open silver MacBook showing DJ software and same "
          "black-and-orange DJ headphones as in @scene. ")
prompts = {
 "A": common + ("Camera at the same position and angle as @scene, about 40 degrees above the desk. The printed A4 workbook "
      "(open size 42 cm wide by 30 cm tall, so the open book is much wider than it is deep, and in perspective each page looks almost square) "
      "now lies OPEN and flat on the desk in the foreground, in the same place, showing two facing pages that are clean plain "
      "bright white matte paper with nothing printed on them, realistic paper thickness, soft gutter shadow in the middle, "
      "visible stacked page edges. Both pages fully visible, entirely inside the frame. Shallow depth of field, workbook sharp, "
      "MacBook softly out of focus. No people, no hands, no text, no watermark."),
 "B": common + ("Camera closer and higher, nearly overhead, about 65 degrees above the desk, looking down at the printed A4 "
      "workbook lying OPEN and flat, upright toward the camera with the spine running vertically from top to bottom through the "
      "center of the frame, left page and right page side by side (each page A4 portrait, 21 by 29.7 cm), filling the frame width, two facing pages of clean plain bright white matte paper with "
      "nothing printed on them, soft gutter shadow, realistic paper thickness. Both pages fully visible inside the frame. "
      "Edge of the MacBook and the headphones partially visible at the top, softly out of focus. "
      "No people, no hands, no text, no watermark."),
}
run("/v1/text_to_image", {
  "model": "gen4_image", "ratio": "720:1280", "seed": 1202, "promptText": prompts[which],
  "referenceImages": [{"uri": data_uri("output/clip01/frame_start.jpg"), "tag": "scene"}],
}, f"output/frames/base_{which}.png")
