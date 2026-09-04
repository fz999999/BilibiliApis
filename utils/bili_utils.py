import hashlib
import time

import execjs

try:
    js = execjs.compile(open('../static/bili.js').read())
except:
    js = execjs.compile(open('static/bili.js').read())

def get_common_headers():
    return {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'cache-control': 'max-age=0',
        'referer': 'https://www.bilibili.com/',
        'sec-ch-ua': '"Microsoft Edge";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0',
    }
def trans_cookies(cookies):
    """Convert a browser Cookie header into a requests-compatible dictionary."""
    if not cookies:
        return {}

    result = {}
    for item in cookies.split(';'):
        item = item.strip()
        if not item or '=' not in item:
            continue
        key, value = item.split('=', 1)
        result[key.strip()] = value.strip()
    return result
def splice_url(params):
    s = ""
    for k, v in params.items():
        s += f"{k}={v}&"
    return s[:-1]

# md5加密 用于生成w_rid
def md5(string):
    m = hashlib.md5()
    m.update(string.encode())
    return m.hexdigest()

def get_search_params(keyword, order, page, qvId):
    return {
        "__refresh__": "true",
        "_extra": "",
        "ad_resource": "5654",
        "category_id": "",
        "context": "",
        "dynamic_offset": str((page - 1) * 24),
        "from_source": "",
        "from_spmid": "333.337",
        "gaia_vtoken": "",
        "highlight": "1",
        "keyword": keyword,
        "order": order,
        "page": page,
        "page_size": "42",
        "platform": "pc",
        "qv_id": qvId,
        "search_type": "video",
        "single_column": "0",
        "source_tag": "3",
        "web_location": "1430654",
        "wts": str(int(time.time())),
    }

def getqvId():
    qvId = js.call('getqvId')
    return qvId

def getW_rid(m):
    on = "ea1db124af3c7062474693fa704f4ff8"
    w_rid = md5(splice_url(m) + on)
    return w_rid