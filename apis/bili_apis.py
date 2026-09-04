import requests
from utils.bili_utils import get_common_headers,  trans_cookies, getqvId, get_search_params, getW_rid

class BiliApis():

    """
        搜索一些内容
        :param keyword: 搜索关键字
        :param order: 排序方式  dm 弹幕数排序 click 播放量排序
        :param cookies_str: cookies字符串
        返回搜索结果
    """
    def search_some(self, keyword, order, page, cookies_str):
        success = True
        msg = "成功"
        res_json = None
        try:
            url = 'https://api.bilibili.com/x/web-interface/wbi/search/type'
            cookies = trans_cookies(cookies_str)
            headers = get_common_headers()
            qvId = getqvId()
            m = get_search_params(keyword, order, page, qvId)
            w_rid = getW_rid(m)
            m["w_rid"] = w_rid
            params = m
            response = requests.get(url, params=params, cookies=cookies, headers=headers)
            res_json = response.json()
        except Exception as e:
            success = False
            msg = str(e)
        return success, msg, res_json

    """
        根据数量搜索一些内容
        :param num: 搜索数量
        :param keyword: 搜索关键字
        :param order: 排序方式  dm 弹幕数排序 click 播放量排序
        :param cookies_str: cookies字符串
        返回搜索结果
    """
    def search_some_by_num(self, num, keyword, order, cookies_str):
        success = True
        msg = "成功"
        work_list = []
        try:
            page = 1
            while True:
                success, msg, res_json = self.search_some(keyword, order, page, cookies_str)
                if not success:
                    break
                work_list.extend(res_json["data"]["result"])
                page += 1
                if page > res_json["data"]["pagesize"] or len(work_list) >= num:
                    break
            if len(work_list) > num:
                work_list = work_list[:num]
        except Exception as e:
            success = False
            msg = str(e)
        return success, msg, work_list

    def get_followings(self, vmid, cookies_str, page_size=50):
        """Get the logged-in user's complete following list and space URLs."""
        success = True
        msg = "成功"
        followings = []

        try:
            cookies = trans_cookies(cookies_str)
            if not cookies.get("SESSDATA"):
                return False, "cookies_str 中缺少有效的 SESSDATA", []

            if vmid is None:
                vmid = cookies.get("DedeUserID")
            if vmid is None or not str(vmid).isdigit() or int(vmid) <= 0:
                return False, "请提供有效的 vmid，或在 Cookie 中包含 DedeUserID", []

            page_size = int(page_size)
            if page_size < 1 or page_size > 50:
                return False, "page_size 必须在 1 到 50 之间", []

            url = "https://api.bilibili.com/x/relation/followings"
            headers = get_common_headers()
            page = 1
            total = None
            seen_mids = set()
            max_pages = 100

            while total is None or len(followings) < total:
                if page > max_pages:
                    return False, f"关注列表超过接口安全分页上限，已获取 {len(followings)}/{total} 条", []
                response = requests.get(
                    url,
                    params={
                        "vmid": str(vmid),
                        "pn": page,
                        "ps": page_size,
                        "order_type": "",
                    },
                    cookies=cookies,
                    headers=headers,
                    timeout=30,
                )
                response.raise_for_status()
                res_json = response.json()

                if res_json.get("code") != 0:
                    return False, res_json.get("message", "获取关注列表失败"), []

                data = res_json.get("data") or {}
                current_page = data.get("list") or []
                total = int(data.get("total") or 0)

                for item in current_page:
                    mid = item.get("mid")
                    if mid is None or str(mid) in seen_mids:
                        continue
                    seen_mids.add(str(mid))
                    following = dict(item)
                    following["space_url"] = f"https://space.bilibili.com/{mid}"
                    followings.append(following)

                if not current_page:
                    if total > len(followings):
                        return False, f"B 站只返回了部分关注列表，已获取 {len(followings)}/{total} 条", []
                    break
                page += 1

            return success, msg, followings
        except (ValueError, TypeError) as e:
            return False, f"参数错误: {e}", []
        except requests.RequestException as e:
            return False, f"请求 B 站接口失败: {e}", []
        except Exception as e:
            return False, str(e), []


if __name__ == '__main__':
    bili_apis = BiliApis()
    cookies_str = r""
    num = 50
    keyword = "娱乐"
    order = "dm"
    success, msg, work_list = bili_apis.search_some_by_num(num, keyword, order, cookies_str)
    print(success, msg, work_list)
    print(len(work_list))


