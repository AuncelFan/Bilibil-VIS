from requests import get
import json
from time import sleep
from .config_parser import data_path, cookies, headers
from .console_log import INFO


def request_history():
    target_url = "https://api.bilibili.com/x/web-interface/history/cursor"
    times = 100
    INFO("Start dumping history.")

    def inf_scroll(_max=0, view_at=0):
        if _max == 0:
            return f"{target_url}?ps=30"
        else:
            return f"{target_url}?ps=30&max={_max}&view_at={view_at}"

    _max = 0
    view_at = 0
    d = []
    for _ in range(times):
        res = get(inf_scroll(_max, view_at), headers=headers, cookies=cookies)
        data = json.loads(res.text)
        _max = data["data"]["cursor"]["max"]
        view_at = data["data"]["cursor"]["view_at"]
        if len(data["data"]["list"]) == 0:
            break
        d += data["data"]["list"]
        # sleep(0.01)

    with open(f"{data_path}bilibili_history.json", "w", encoding="utf-8") as f:
        json.dump(d, f, indent=4, ensure_ascii=False)
    INFO(f"Get {len(d)} history records.")

