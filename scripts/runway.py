"""Minimal Runway API client (documented params only, X-Runway-Version 2024-11-06)."""
import base64, json, mimetypes, os, sys, time, urllib.request

BASE = "https://api.dev.runwayml.com"


def _key():
    k = os.environ.get("RUNWAYML_API_SECRET")
    if not k:
        env = os.path.join(os.path.dirname(__file__), "..", ".env")
        for line in open(env):
            if line.startswith("RUNWAYML_API_SECRET="):
                k = line.split("=", 1)[1].strip()
    return k


def _req(method, path, body=None):
    data = json.dumps(body).encode() if body is not None else None
    r = urllib.request.Request(BASE + path, data=data, method=method, headers={
        "Authorization": f"Bearer {_key()}",
        "X-Runway-Version": "2024-11-06",
        "Content-Type": "application/json",
    })
    try:
        with urllib.request.urlopen(r) as resp:
            return json.loads(resp.read() or b"{}")
    except urllib.error.HTTPError as e:
        sys.exit(f"HTTP {e.code}: {e.read().decode()}")


def data_uri(path):
    mime = mimetypes.guess_type(path)[0]
    return f"data:{mime};base64," + base64.b64encode(open(path, "rb").read()).decode()


def run(path, body, out):
    task = _req("POST", path, body)
    tid = task["id"]
    print("task", tid, flush=True)
    delay = 5
    while True:
        time.sleep(delay)
        t = _req("GET", f"/v1/tasks/{tid}")
        print(t["status"], t.get("progress", ""), flush=True)
        if t["status"] == "SUCCEEDED":
            urllib.request.urlretrieve(t["output"][0], out)
            print("saved", out, "cost", t.get("cost"))
            return t
        if t["status"] in ("FAILED", "CANCELLED"):
            sys.exit(f"{t['status']}: {t.get('failure')} {t.get('failureCode')}")
        delay = min(delay + 2, 15)
