import sys; sys.path.insert(0, "scripts")
from runway import run, data_uri
model = sys.argv[1] if len(sys.argv) > 1 else "gen4_turbo"
prompt = (
 "Slow, smooth cinematic push-in toward the printed workbook lying on the desk; the camera glides gently forward "
 "and slightly down, keeping the workbook cover sharp and unchanged while the MacBook and headphones stay softly "
 "out of focus behind. Near the end, one realistic human hand with five fingers slowly enters from the right edge "
 "of the frame and rests lightly beside the right edge of the workbook. Calm, elegant, steady camera, no shake, "
 "no zoom jumps. The cover artwork does not change. No text overlays, no captions, no watermark."
)
run("/v1/image_to_video", {
  "model": model, "ratio": "720:1280", "duration": 3, "seed": 1201, "promptText": prompt,
  "promptImage": data_uri("output/clip01/frame_start.jpg"),
}, f"output/clip01/clip01_capa_{model}.mp4")
