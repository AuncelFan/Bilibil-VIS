import json
from datetime import datetime
from .config_parser import data_path
from .console_log import INFO


def reduce_data():
    with open(f"{data_path}bilibili_history.json", "r", encoding="utf-8") as f:
        history = json.load(f)
    with open(f"{data_path}follow.json", "r", encoding="utf-8") as f:
        follow = json.load(f)
    with open(f"{data_path}relation.json", "r", encoding="utf-8") as f:
        relation = json.load(f)
    
    follow_set = set(item['mid'] for item in follow['data']['list'])  # all followed mid
    result = []
    for raw in history:
        item = {}
        item['title'] = raw['title']
        item['business'] = raw['history']['business']
        item['bvid'] = raw['history']['bvid']
        item['dt'] = raw['history']['dt']
        item['videos'] = raw['videos']
        item['author_name'] = raw['author_name']
        item['author_mid'] = raw['author_mid']
        item['view_at'] = raw['view_at']
        view_at_dt = datetime.fromtimestamp(raw['view_at'])
        item['view_at_parsed'] = {'week': view_at_dt.weekday(),
                                  'hour': view_at_dt.hour,
                                  'minute': view_at_dt.minute,
                                  'second': view_at_dt.second,
                                  'year': view_at_dt.year,
                                  'month': view_at_dt.month,
                                  'day': view_at_dt.day,
                                  'time': view_at_dt.hour * 10000 + view_at_dt.minute * 100 + view_at_dt.second,
                                  'date': view_at_dt.year * 10000 + view_at_dt.month * 100 + view_at_dt.day}
        if raw['duration'] == 0 or raw['progress'] == -1:
            item['progress'] = 100.0
        else :
            item['progress'] = 100 * raw['progress'] / raw['duration']
        item['duration'] = raw['duration']
        item['is_fav'] = raw['is_fav']
        item['kid'] = raw['kid']
        item['tag_name'] = raw['tag_name']
        if item['bvid'] in relation:
            relate = relation[item['bvid']]
            item['like'] = relate['like']
            item['coin'] = relate['coin']
            item['dislike'] = relate['dislike']
        else:
            item['like'] = False
            item['coin'] = 0
            item['dislike'] = False
        item['follow'] = raw['author_mid'] in follow_set
        result.append(item)

    with open(f"{data_path}main_data.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4, ensure_ascii=False)
    
    INFO("Finished parsing data")
