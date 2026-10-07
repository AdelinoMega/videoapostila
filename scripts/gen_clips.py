"""Generate all six clips with veo3.1 (first + last keyframes = composed frames with REAL pages).
usage: python3 scripts/gen_clips.py <clip_key>"""
import sys; sys.path.insert(0, "scripts")
from runway import run, data_uri

F = "output/frames/"
STYLE = (" Photorealistic, cinematic premium product commercial, warm soft key light, subtle blue and orange background accents, "
         "shallow depth of field, calm elegant movement, steady camera. The printed pages stay exactly as they are: same "
         "layout, same pictures, same colors. Only hands and forearms of a person, never a face. No text overlays, no captions, no watermark.")
NEG = ("invented pages, changing page content, gibberish text, distorted letters, altered logos, different cover, blank pages, "
       "extra fingers, missing fingers, merged fingers, deformed hands, face, head, plastic or transparent paper, multiple pages "
       "flying, warped laptop, cartoon, 3D render, anime, captions, subtitles, watermark, camera shake, fast zoom, whip pan, overexposure")
CLIPS = {
 "clip01_capa": ("c01_start", "c01_end",
   "Slow, smooth cinematic push-in toward the closed printed workbook lying on the desk, the camera glides gently forward. "
   "The real cover stays sharp and unchanged; the MacBook with DJ software and the headphones remain softly out of focus behind. No hands."),
 "clip02_abrindo": ("closed_cover", "A_02_03",
   "One continuous shot, no cuts. A realistic hand with five fingers enters from the right, holds the right edge of the closed "
   "workbook's front cover and slowly lifts it; the cover swings over the spine to the left with natural weight and lands flat on the "
   "desk, so the workbook lies open on its first spread: on the left the inside dark blue title page with a man's portrait, on the "
   "right the white welcome page. The camera gently eases back to keep the whole open workbook in frame. The hand withdraws out of frame."),
 "clip03_folheando": ("A_02_03", "A_06_14",
   "One continuous shot, no cuts. A hand takes the lower right corner of the white right-hand page and turns exactly that one sheet "
   "from right to left in a single slow motion. The reverse side of that same sheet is a dark blue page with a man's portrait and DJ "
   "turntables at the bottom; it lands on the left, covering the old left page. Underneath, the new right-hand page is revealed: a white "
   "page with a dark controller diagram at the top. No other pages turn; the hand leaves the frame."),
 "clip04_serato": ("A_68_102", "A_68_102",
   "The workbook lies open in the foreground. A left hand rests calmly on the left page while a right hand reaches to the MacBook "
   "trackpad and slides a finger on it. Rack focus: the focus slowly shifts from the workbook to the MacBook screen showing DJ software "
   "with two decks and waveforms, then returns to the workbook. Both hands then withdraw out of frame. The pages do not move."),
 "clip05_tecnico": ("Az_50_137", "Az_14_95",
   "Closer, slightly higher view of the open workbook. A hand lifts the right-hand page by its lower corner and slowly turns exactly one "
   "sheet from right to left, the paper flexing naturally with its printed reverse side visible, revealing the colorful circular chart page "
   "on the right; the sheet settles and the hand leaves the frame."),
 "clip06_final": ("Az_14_95", "A_14_95",
   "Gentle cinematic pull-back with a very slight lateral move, revealing the whole desk: the open workbook as the hero in the foreground, "
   "the MacBook with DJ software behind and the headphones at the side. Nothing on the desk moves, no hands. Clean, calm final composition."),
}
key = sys.argv[1]
SEED = int(sys.argv[2]) if len(sys.argv) > 2 else 1201
first, last, prompt = CLIPS[key]
run("/v1/image_to_video", {
  "model": "veo3.1", "ratio": "720:1280", "duration": 4, "audio": False, "seed": SEED,
  "promptText": prompt + STYLE, "negativePrompt": NEG,
  "promptImage": [{"uri": data_uri(F + first + ".jpg"), "position": "first"},
                  {"uri": data_uri(F + last + ".jpg"), "position": "last"}],
}, f"output/final/{key}.mp4")
