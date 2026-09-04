import uvicorn
from apis.bili_apis import BiliApis
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

apis = BiliApis()
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


"""
    搜索一些内容
    :json num: 搜索数量
    :json keyword: 搜索关键字
    :json order: 排序方式  dm 弹幕数排序 click 播放量排序
    :json cookies_str: cookies字符串    
"""
@app.post("/search_some_by_num")
def search_some_by_num(data: dict):
    try:
        num = data["num"]
        keyword = data["keyword"]
        order = data["order"]
        cookies_str = data["cookies_str"]
        success, msg, work_list = apis.search_some_by_num(num, keyword, order, cookies_str)
        if success:
            return {"code": 200, "message": msg, "data": work_list}
        else:
            return {"code": 400, "message": msg, "data": None}
    except Exception as e:
        return {"code": 400, "message": str(e), "data": None}


@app.post("/popular_videos")
def popular_videos(data: dict):
    try:
        success, msg, result = apis.get_popular_videos(
            data.get("page", 1), data.get("page_size", 20), data.get("cookies_str", "")
        )
        return {"code": 200 if success else 400, "message": msg, "data": result if success else None}
    except Exception as e:
        return {"code": 400, "message": str(e), "data": None}


@app.post("/user_card")
def user_card(data: dict):
    try:
        success, msg, result = apis.get_user_card(data.get("mid"), data.get("cookies_str", ""))
        return {"code": 200 if success else 400, "message": msg, "data": result if success else None}
    except Exception as e:
        return {"code": 400, "message": str(e), "data": None}


@app.post("/space_navnum")
def space_navnum(data: dict):
    try:
        success, msg, result = apis.get_space_navnum(data.get("mid"), data.get("cookies_str", ""))
        return {"code": 200 if success else 400, "message": msg, "data": result if success else None}
    except Exception as e:
        return {"code": 400, "message": str(e), "data": None}


@app.post("/relation_stat")
def relation_stat(data: dict):
    try:
        success, msg, result = apis.get_relation_stat(data.get("mid"), data.get("cookies_str", ""))
        return {"code": 200 if success else 400, "message": msg, "data": result if success else None}
    except Exception as e:
        return {"code": 400, "message": str(e), "data": None}


@app.post("/video_info")
def video_info(data: dict):
    try:
        success, msg, result = apis.get_video_info(
            data.get("bvid"), data.get("aid"), data.get("cookies_str", "")
        )
        return {"code": 200 if success else 400, "message": msg, "data": result if success else None}
    except Exception as e:
        return {"code": 400, "message": str(e), "data": None}


@app.post("/video_tags")
def video_tags(data: dict):
    try:
        success, msg, result = apis.get_video_tags(
            data.get("bvid"), data.get("aid"), data.get("cookies_str", "")
        )
        return {"code": 200 if success else 400, "message": msg, "data": result if success else None}
    except Exception as e:
        return {"code": 400, "message": str(e), "data": None}


@app.post("/related_videos")
def related_videos(data: dict):
    try:
        success, msg, result = apis.get_related_videos(
            data.get("bvid"), data.get("aid"), data.get("cookies_str", "")
        )
        return {"code": 200 if success else 400, "message": msg, "data": result if success else None}
    except Exception as e:
        return {"code": 400, "message": str(e), "data": None}


@app.post("/video_comments")
def video_comments(data: dict):
    try:
        success, msg, result = apis.get_video_comments(
            data.get("oid"),
            data.get("page", 1),
            data.get("page_size", 20),
            data.get("sort", 2),
            data.get("cookies_str", ""),
        )
        return {"code": 200 if success else 400, "message": msg, "data": result if success else None}
    except Exception as e:
        return {"code": 400, "message": str(e), "data": None}


@app.post("/get_followings")
def get_followings(data: dict):
    """Return all visible followings for the logged-in Bilibili account."""
    try:
        cookies_str = data.get("cookies_str", "")
        vmid = data.get("vmid")
        page_size = data.get("page_size", 50)
        success, msg, followings = apis.get_followings(vmid, cookies_str, page_size)
        if not success:
            return {"code": 400, "message": msg, "data": None}

        return {
            "code": 200,
            "message": msg,
            "data": {
                "total": len(followings),
                "items": followings,
                "space_urls": [item["space_url"] for item in followings],
            },
        }
    except Exception as e:
        return {"code": 400, "message": str(e), "data": None}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5008, forwarded_allow_ips='*')
