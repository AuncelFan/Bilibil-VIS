from requests import get
import json
from .config_parser import mid, data_path, cookies, headers
from .console_log import INFO

def request_follow():
    res = get(f"https://api.bilibili.com/x/relation/followings?vmid={mid}", headers=headers, cookies=cookies)
    a = json.loads(res.text)
    with open(f"{data_path}follow.json", "w", encoding="utf-8") as f:
        json.dump(a, f, indent=4, ensure_ascii=False)
    INFO(f"Get follow data for {mid}")