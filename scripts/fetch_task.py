"""Re-download a finished task's output: python3 scripts/fetch_task.py <task_id> <out_path>"""
import sys, urllib.request; sys.path.insert(0, "scripts")
from runway import _req
t = _req("GET", f"/v1/tasks/{sys.argv[1]}")
print(t["status"]); urllib.request.urlretrieve(t["output"][0], sys.argv[2]); print("saved", sys.argv[2])
