import json
from time import sleep
from requests import get
from .config_parser import data_path, cookies, headers, debug_mode
from .console_log import INFO, WARN, ERROR



def request_relations():
    with open(f"{data_path}bilibili_history.json", "r", encoding="utf-8") as f:
        data = json.loads(f.read())
    try:
        with open(f"{data_path}relation.json", "r", encoding="utf-8") as f:
            result = json.loads(f.read())
        INFO(f"Read stored data, length is {len(result)}")
    except Exception:
        result = {}
    counter = 0
    
    for item in data:
        try:
            bvid = item['history']['bvid']
            if bvid == "":  # text and live does not have bvid
                continue
            if bvid in result:
                if debug_mode:
                    WARN("video exist")
                continue
            res = get(f"https://api.bilibili.com/x/web-interface/archive/relation?bvid={bvid}", cookies=cookies, headers=headers)
            res = json.loads(res.text)['data']
            result[bvid] = res
            # sleep(0.1)
            counter += 1
            if counter % 100 == 0:
                INFO(f"Parsing data No.{counter}")
        except Exception as e:
            ERROR(f"Error at No.{counter}: {e}, item={item}, res={res}")
    
    
    with open(f"{data_path}relation.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4, ensure_ascii=False)
    INFO(f"Finished getting relation data. Now lenth is {len(result)}")
