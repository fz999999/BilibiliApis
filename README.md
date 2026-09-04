<div align="center">
    <a href="https://www.python.org/">
        <img src="https://img.shields.io/badge/python-3.12%2B-blue" alt="Python 3.12+">
    </a>
    <a href="https://nodejs.org/zh-cn/">
        <img src="https://img.shields.io/badge/nodejs-20%2B-green" alt="NodeJS 20+">
    </a>
    <a href="https://fastapi.tiangolo.com/">
        <img src="https://img.shields.io/badge/FastAPI-0.115%2B-009688" alt="FastAPI">
    </a>
</div>

# 🎬 Bilibili Platform

**✨ 专业的 B站 视频数据采集解决方案，支持按关键词批量搜索视频信息**

当你需要让 AI Agent 感知 B站内容生态——自动采集视频热度、分析弹幕趋势、驱动内容运营策略——第一道墙往往不是模型能力，而是**平台数据获取能力的缺失**。

本项目做的事很简单：把这道墙拆掉。

**⚠️ 严禁用于爬取用户隐私、违规商业用途！本项目仅供学习与技术研究使用，后果自负。**

## 🌟 功能特性

- ✅ **视频搜索采集**
  - 按关键词批量搜索视频
  - 支持按播放量 / 弹幕数排序
  - 自动翻页，按需获取指定数量结果
- 🔐 **WBI 签名自动计算**
  - 内嵌 JS 运行时，自动生成 `w_rid` 签名参数
  - 适配 B站最新 WBI 鉴权接口
- 🚀 **高性能服务**
  - 基于 FastAPI + Uvicorn 异步服务
  - 支持 Docker 一键部署

## 🛠️ 快速开始

### ⛳ 运行环境

- Python 3.12+
- Node.js 20+


### 🎯 本地安装

```bash
pip install -r requirements.txt
```

### 🚀 运行项目

```bash
python App.py
```

服务启动后访问 http://localhost:5008/docs 查看交互式 API 文档。

### 🎨 Cookie 配置

在浏览器中打开 [www.bilibili.com](https://www.bilibili.com)，**登录账号**后按 `F12` 打开开发者工具，点击「网络」→ 找任意一个接口请求 → 复制请求头中的 `Cookie` 字段值。

> ⚠️ 注意：必须登录后获取的 Cookie 才有效，未登录的 Cookie 无法正常请求搜索接口。

将获取到的 Cookie 字符串作为 `cookies_str` 参数传入接口，格式如下：

```
SESSDATA=xxx; bili_jct=xxx; DedeUserID=xxx; ...
```

## 📡 接口说明

### POST `/search_some_by_num`

按数量批量搜索 B站 视频。

**请求参数**

| 字段          | 类型  | 必填 | 说明                                  |
|-------------|-----|----|-------------------------------------|
| keyword     | str | 是  | 搜索关键词                               |
| num         | int | 是  | 期望返回的视频数量                           |
| order       | str | 是  | 排序方式：`dm`（弹幕数）/ `click`（播放量）       |
| cookies_str | str | 是  | B站登录 Cookie 字符串                     |

**请求示例**

```bash
curl -X POST http://localhost:5008/search_some_by_num \
  -H "Content-Type: application/json" \
  -d '{
    "keyword": "编程教学",
    "num": 20,
    "order": "click",
    "cookies_str": "SESSDATA=xxx; bili_jct=xxx; DedeUserID=xxx"
  }'
```

**响应示例**

```json
{
  "code": 200,
  "message": "成功",
  "data": [
    {
      "aid": 123456789,
      "bvid": "BVxxxxxxxx",
      "title": "视频标题",
      "author": "UP主名称",
      "play": 100000,
      "video_review": 5000
    }
  ]
}
```

### POST `/get_followings`

读取登录 Cookie 对应账号的关注列表，并为每个关注用户生成空间网址。`vmid` 可以省略，省略时会从 Cookie 中的 `DedeUserID` 自动读取。该接口面向 Cookie 所属的当前账号；如果 B 站返回的数量少于声明总数，服务会返回错误提示，避免误报为完整列表。

**请求参数**

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| cookies_str | str | 是 | B 站登录 Cookie，需包含有效的 `SESSDATA`；省略 `vmid` 时还需包含 `DedeUserID` |
| vmid | int/str | 否 | 当前账号的 mid；不传时使用 Cookie 中的 `DedeUserID` |
| page_size | int | 否 | 每页数量，范围 `1-50`，默认 `50` |

**请求示例**

```bash
curl -X POST http://localhost:5008/get_followings \\
  -H "Content-Type: application/json" \\
  -d '{
    "cookies_str": "SESSDATA=xxx; bili_jct=xxx; DedeUserID=123456"
  }'
```

**响应示例**

```json
{
  "code": 200,
  "message": "成功",
  "data": {
    "total": 1,
    "items": [
      {
        "mid": 3546911978031307,
        "uname": "示例用户",
        "space_url": "https://space.bilibili.com/3546911978031307"
      }
    ],
    "space_urls": [
      "https://space.bilibili.com/3546911978031307"
    ]
  }
}
```

## 🍥 日志

| 日期       | 说明                            |
|----------|---------------------------------|
| 26/04/10 | 项目初始化，完成视频搜索 API 封装            |


## 🤝 欢迎贡献 PR

本项目欢迎任何形式的贡献！如果你有新功能想法、Bug 修复或文档改进，欢迎提交 PR。

- Fork 本仓库并在新分支上开发
- 保持代码风格与现有代码一致
- PR 描述中请简要说明改动内容和目的
- 也欢迎通过 [Issue](https://github.com/cv-cat/BilibiliApis/issues) 提出建议或报告问题

## 🧸额外说明
1. 感谢star⭐和follow📰！不时更新
2. 作者的联系方式在主页里，有问题可以随时联系我
3. 可以关注下作者的其他项目，欢迎 PR 和 issue
4. 感谢赞助！如果此项目对您有帮助，请作者喝一杯奶茶~~ （开心一整天😊😊）
5. thank you~~~


## 📈 Star 趋势

<a href="https://cvcat.site/star-history/svg?repos=cv-cat/BilibiliApis&type=Date">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://cvcat.site/star-history/svg?repos=cv-cat/BilibiliApis&type=Date&theme=dark" />
    <source media="(prefers-color-scheme: light)" srcset="https://cvcat.site/star-history/svg?repos=cv-cat/BilibiliApis&type=Date" />
    <img alt="Star History Chart" src="https://cvcat.site/star-history/svg?repos=cv-cat/BilibiliApis&type=Date" />
  </picture>
</a>


## 🍔 交流群

如果你对爬虫和 AI Agent 感兴趣，可以加入群聊一起讨论~

ps: 请加群，人满或者过期 issue | wx 提醒 | qq提醒

| group-1 | group-2 | group-3 | group-4 (2000人qq群) |
|:--:|:--:|:--:|:--:|
| <img width="280" alt="group1" src="https://cvcat.site/assets/group1.jpg" /> | <img width="280" alt="group2" src="https://cvcat.site/assets/group2.jpg" /> | <img width="280" alt="group3" src="https://cvcat.site/assets/group3.jpg" /> | <img width="280" alt="group3" src="https://cvcat.site/assets/group4.jpg" /> |
