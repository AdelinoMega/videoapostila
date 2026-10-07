import sys; sys.path.insert(0, "scripts")
from runway import run, data_uri
prompt = (
 "Photorealistic cinematic product photo, vertical. Modern home-studio study desk, warm soft key light, "
 "subtle blue and orange accents in the dark background. In the foreground, lying flat on the wooden desk, a closed "
 "printed A4 full-color workbook (matte premium paper, realistic thickness, visible page edges) whose front cover is exactly @cover, "
 "unchanged, fully visible, seen from about 40 degrees above. Behind it, softly out of focus, an open silver MacBook showing "
 "DJ software with two decks, waveforms and a music library. Professional DJ headphones at the side of the desk. "
 "Shallow depth of field, focus on the workbook cover. No people, no hands, no text overlays, no watermark."
)
run("/v1/text_to_image", {
  "model": "gen4_image", "ratio": "720:1280", "promptText": prompt, "seed": 1201,
  "referenceImages": [{"uri": data_uri("output/clip01/ref_cover.jpg"), "tag": "cover"}],
}, "output/clip01/frame_raw.png")
