# -*- coding: utf-8 -*-
"""生成《接口总览-客户版》图（HTML -> PNG）。

数据源：接口清单-完整版.md 附录 C（125 条完整清单）
        剔除客户版隐藏的 4 条（InviteGroupMember / AcceptFriendRequest /
        SetContactRemarkOplog / SetContactRemarkNative）= 121 条

输出：  static/img/api-overview.png

用法：  python tools/gen_api_overview.py
"""

from __future__ import annotations

import os
import subprocess
import sys
import traceback
from pathlib import Path

import pandas as pd
from loguru import logger

ROOT = Path(__file__).resolve().parent.parent
IMG_DIR = ROOT / "static" / "img"
OUT_HTML = IMG_DIR / "api-overview.html"
OUT_PNG = IMG_DIR / "api-overview.png"

# 版式参数
WIDTH = 1240              # 逻辑宽度（截图时乘 device_scale_factor）
SCALE = 2                 # 2x 高清
COLUMNS = 3               # 分栏数
CANVAS_H = 3000           # 先按足够高截图，再按内容自动裁掉底部空白
BG = "#0b0e14"

LOGO = "WXHOOK"
TITLE = "完整接口版 · 客户版"
SUBTITLE = "Windows WeChat 4.1.15.56 · 本地 HTTP 接口 http://127.0.0.1:30001"
FOOTER_LEFT = "版本：客户版（自用版 125 条，客户版可见 121 条）"
FOOTER_RIGHT = "以 /WxApi/Catalog 的实时输出为准"

# 分组 -> [(路由, 方法)]，顺序与《接口清单-完整版.md》附录 C 一致
GROUPS: list[tuple[str, list[tuple[str, str]]]] = [
    (
        "账号",
        [
            ("/IsLoginStatus", "POST/GET"),
            ("/getonlineinfo", "POST/GET"),
            ("/GetSelfProfile", "POST"),
            ("/GetQRCode", "POST/GET"),
            ("/GetGroupQRCode", "POST/GET"),
            ("/SendQRCode", "POST"),
        ],
    ),
    ("会话", [("/api/session", "POST/GET")]),
    (
        "联系人",
        [
            ("/SetContactRemark", "POST"),
            ("/SearchContact", "POST"),
            ("/GetContact", "POST"),
            ("/GetFriendOrChatroomDetailInfo", "POST"),
            ("/GetContactList", "POST"),
            ("/BatchGetContactBriefInfo", "POST"),
            ("/QueryBodyInfo", "POST"),
            ("/GetContactLabelList", "POST"),
            ("/GetHeadIMG", "POST"),
            ("/CheckFriendStatus", "POST"),
            ("/api/contact/extra", "POST/GET"),
            ("/AddFriend", "POST"),
            ("/DelFriend", "POST"),
            ("/GetContactLabelMap", "GET"),
            ("/GetLabelList", "GET"),
            ("/AddLabel", "POST"),
            ("/UpdateLabel", "POST"),
            ("/DelLabel", "POST"),
            ("/SetContactLabels", "POST"),
            ("/GetContactLabels", "GET"),
        ],
    ),
    (
        "群",
        [
            ("/DelGroupMember", "POST"),
            ("/AddGroupMember", "POST"),
            ("/SetGroupAnnouncement", "POST"),
            ("/CreateGroup", "POST"),
            ("/QuitGroup", "POST"),
            ("/SetGroupName", "POST"),
            ("/SetMyGroupNick", "POST"),
            ("/QueryChatRoomList", "POST/GET"),
            ("/QueryChatRoomMemberCount", "POST"),
            ("/BatchGetChatRoomMemberWxid", "POST"),
            ("/QueryChatRoomMemberNickName", "POST"),
            ("/QueryChatRoomOwnerWxid", "POST"),
            ("/GetChatrooMmemberDetail", "POST"),
            ("/GetChatroomMemberDetailInfo", "POST"),
        ],
    ),
    (
        "消息",
        [
            ("/api/message_cache", "POST/GET"),
            ("/GetRevoked", "POST/GET"),
            ("/SetCallback", "POST"),
            ("/Zstd", "POST/GET"),
            ("/RecentMessages", "GET"),
            ("/MsgStats", "GET/POST"),
            ("/Events", "GET"),
            ("/MsgImage", "GET"),
            ("/MsgQuote", "POST"),
            ("/MsgTypes", "POST/GET"),
            ("/api/callog", "POST/GET"),
        ],
    ),
    (
        "发送",
        [
            ("/SendVideoMsg", "POST"),
            ("/TestSend", "POST"),
            ("/ReplyRules", "GET/POST"),
            ("/BotSwitch", "GET/POST"),
            ("/SendTextMsg", "POST"),
            ("/SendTextMsg_NoSrc", "POST"),
            ("/SendAtMsg_NoSrc", "POST"),
            ("/SendImgMsg", "POST"),
            ("/SendImgMsg_NoSrc", "POST"),
            ("/ForwardXMLMsg", "POST/GET"),
            ("/ForwardMsg", "POST/GET"),
            ("/SendLinkCard", "POST"),
            ("/Forward", "POST"),
            ("/SendFileFromMessage", "POST"),
            ("/SendXml", "POST"),
            ("/SendVoice", "POST"),
            ("/SendVoiceFromAudio", "POST"),
            ("/SendGuard", "POST/GET"),
            ("/SendPat", "POST"),
        ],
    ),
    (
        "朋友圈",
        [
            ("/SnsUserPageSync", "POST/GET"),
            ("/SnsObjectDetail", "POST/GET"),
            ("/SnsComment", "POST/GET"),
            ("/SnsObjectOp", "POST/GET"),
            ("/SnsStickyOnTop", "POST"),
            ("/SnsTopList", "GET"),
            ("/SnsMedia", "POST/GET"),
            ("/TimelineGetFristPage", "POST/GET"),
            ("/TimelineGetNextPage", "POST/GET"),
            ("/mmsnsuserpage", "POST/GET"),
            ("/GetFriendTimeline", "POST/GET"),
            ("/get_moments", "POST/GET"),
            ("/get_friend_moments", "POST/GET"),
            ("/api/sns/extra", "POST/GET"),
            ("/PublishMoments", "POST"),
        ],
    ),
    (
        "媒体/文件",
        [
            ("/AttachFile", "GET"),
            ("/RevokedFile", "GET"),
            ("/MsgMedia", "GET"),
            ("/CdnMedia", "GET"),
            ("/DownloadFile", "POST"),
            ("/SendCdnMedia", "POST"),
            ("/ForwardMedia", "POST"),
            ("/api/media", "POST/GET"),
            ("/Decode_Pic", "POST"),
            ("/FindImageKey", "POST/GET"),
            ("/download", "POST/GET"),
            ("/downloadbigfile", "POST/GET"),
            ("/DownloadVoice", "POST/GET"),
            ("/VoiceData", "GET/POST"),
            ("/VoiceInfo", "GET/POST"),
            ("/RevokedImage", "GET"),
        ],
    ),
    (
        "收藏",
        [
            ("/GetFavList", "POST"),
            ("/Batchgetfavitem", "POST"),
        ],
    ),
    (
        "支付/红包",
        [
            ("/api/payment", "POST/GET"),
            ("/PaymentStats", "POST/GET"),
        ],
    ),
    (
        "系统/诊断",
        [
            ("/AdminGate", "GET/POST"),
            ("/GetPushOptions", "GET"),
            ("/NotifyStats", "GET/POST"),
            ("/api/db", "POST/GET"),
            ("/QueryDB/execute", "POST"),
            ("/QueryDB/GetAllDBName", "POST"),
            ("/QueryDB/status", "GET"),
            ("/WxLayout", "POST/GET"),
            ("/FaultLog", "POST/GET"),
            ("/AntiRevokeHook", "POST/GET"),
            ("/AntiRevokeRecipe", "POST/GET"),
            ("/WxApi/Routes", "GET"),
            ("/WxApi/Catalog", "GET"),
            ("/", "GET"),
        ],
    ),
    ("其他", [("/api/other", "POST/GET")]),
]

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<title>{title}</title>
<style>
  * {{ box-sizing: border-box; }}
  html, body {{
    margin: 0; padding: 0;
    background: {bg};
    color: #c9d1d9;
    -webkit-font-smoothing: antialiased;
  }}
  body {{
    font-family: "Segoe UI", "Microsoft YaHei UI", "Microsoft YaHei", sans-serif;
    width: {width}px;
  }}
  .page {{ padding: 26px 32px 18px; }}
  header {{
    display: flex; align-items: center; gap: 16px;
    padding-bottom: 13px;
    border-bottom: 1px solid #1e2430;
  }}
  .brand {{
    font-size: 27px; font-weight: 800; letter-spacing: 2px;
    color: #e6edf3; font-family: ui-monospace, Consolas, monospace;
  }}
  .divider {{ width: 1px; height: 26px; background: #262d3a; }}
  .title {{ font-size: 19px; font-weight: 600; color: #9aa4b2; letter-spacing: 1px; }}
  .count {{
    margin-left: auto; font-size: 13px; color: #c9d1d9;
    border: 1px solid #303845; border-radius: 8px;
    padding: 6px 14px; background: #141a22;
  }}
  .subtitle {{ margin: 9px 0 0; font-size: 12px; color: #6e7681; }}
  .cols {{
    display: grid;
    grid-template-columns: repeat({col_count}, 1fr);
    gap: 0 34px;
    margin-top: 14px;
    align-items: start;
  }}
  .group {{ margin-bottom: 14px; break-inside: avoid; }}
  .group h2 {{
    margin: 0 0 4px; font-size: 14px; font-weight: 700;
    color: #9aa4b2; letter-spacing: 1px;
    display: flex; align-items: baseline; gap: 7px;
  }}
  .group h2 .n {{ font-size: 11.5px; font-weight: 500; color: #59616e; }}
  .row {{
    display: flex; align-items: center; justify-content: space-between;
    gap: 8px; padding: 2.5px 1px;
    border-bottom: 1px dashed #161b24;
    font-family: ui-monospace, Consolas, "Cascadia Mono", monospace;
    font-size: 12.5px;
  }}
  .route {{ color: #c3cddb; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}
  .chips {{ display: flex; gap: 4px; flex: none; }}
  .chip {{
    font-size: 9.5px; line-height: 15px; letter-spacing: .3px;
    color: #6f7a89; border: 1px solid #262e3b;
    border-radius: 4px; padding: 0 5px; background: #10151c;
  }}
  footer {{
    display: flex; justify-content: space-between; align-items: center;
    margin-top: 14px; padding-top: 11px;
    border-top: 1px solid #1e2430;
    font-size: 11.5px; color: #5c6572;
    font-family: ui-monospace, Consolas, monospace;
  }}
</style>
</head>
<body>
<div class="page">
  <header>
    <span class="brand">{logo}</span>
    <span class="divider"></span>
    <span class="title">{title}</span>
    <span class="count">{total} 个接口</span>
  </header>
  <p class="subtitle">{subtitle}</p>
  <div class="cols">
{columns}
  </div>
  <footer>
    <span>{footer_left}</span>
    <span>{footer_right}</span>
  </footer>
</div>
</body>
</html>
"""

GROUP_TEMPLATE = """    <div class="group">
      <h2>{name} <span class="n">{n}</span></h2>
{rows}
    </div>"""

ROW_TEMPLATE = (
    '      <div class="row"><span class="route">{route}</span>'
    '<span class="chips">{chips}</span></div>'
)


def build_dataframe() -> pd.DataFrame:
    """把分组数据整理成一张表，便于统计与渲染。"""
    records = []
    for gname, routes in GROUPS:
        for route, method in routes:
            records.append({"group": gname, "route": route, "method": method})
    return pd.DataFrame(records, columns=["group", "route", "method"])


def split_columns() -> list[list[tuple[str, list[tuple[str, str]]]]]:
    """按分组顺序切成 N 栏，选行数最均衡的切法（分组不拆断）。"""
    counts = [len(routes) for _, routes in GROUPS]
    n = len(GROUPS)
    k = COLUMNS
    if k <= 1 or n <= k:
        return [GROUPS]

    best_splits: list[int] | None = None
    best_key: tuple[int, int] | None = None
    from itertools import combinations

    for cuts in combinations(range(1, n), k - 1):
        bounds = (0, *cuts, n)
        sums = [sum(counts[bounds[i] : bounds[i + 1]]) for i in range(k)]
        key = (max(sums) - min(sums), max(sums))
        if best_key is None or key < best_key:
            best_key, best_splits = key, list(bounds)

    assert best_splits is not None
    cols = []
    for i in range(k):
        cols.append(GROUPS[best_splits[i] : best_splits[i + 1]])
    return cols


def render_group(name: str, routes: list[tuple[str, str]]) -> str:
    rows = "\n".join(
        ROW_TEMPLATE.format(
            route=route,
            chips="".join('<span class="chip">%s</span>' % m for m in method.split("/")),
        )
        for route, method in routes
    )
    return GROUP_TEMPLATE.format(name=name, n=len(routes), rows=rows)


def build_columns_html() -> str:
    cols = split_columns()
    blocks = []
    for col in cols:
        inner = "\n".join(render_group(name, routes) for name, routes in col)
        blocks.append('  <div class="col">\n%s\n  </div>' % inner)
    return "\n".join(blocks)


def find_browser() -> str:
    candidates = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    ]
    for path in candidates:
        if os.path.exists(path):
            return path
    raise FileNotFoundError("未找到 Chrome / Edge，无法截图")


def screenshot() -> None:
    browser = find_browser()
    if OUT_PNG.exists():
        OUT_PNG.unlink()
    cmd = [
        browser,
        "--headless=new",
        "--disable-gpu",
        "--hide-scrollbars",
        "--no-first-run",
        "--no-default-browser-check",
        f"--force-device-scale-factor={SCALE}",
        f"--window-size={WIDTH},{CANVAS_H}",
        f"--screenshot={OUT_PNG}",
        OUT_HTML.as_uri(),
    ]
    logger.info(f"截图：{Path(browser).name} {WIDTH}x{CANVAS_H}@{SCALE}x")
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
    if proc.returncode != 0 or not OUT_PNG.exists():
        raise RuntimeError(
            f"截图失败 rc={proc.returncode}\n"
            f"stdout={proc.stdout[-800:]}\nstderr={proc.stderr[-800:]}"
        )


def crop_bottom() -> None:
    """裁掉底部多余背景，只保留内容 + 少量留白。"""
    from PIL import Image

    bg = tuple(int(BG.lstrip("#")[i : i + 2], 16) for i in (0, 2, 4))
    img = Image.open(OUT_PNG).convert("RGB")
    w, h = img.size
    pixels = img.load()
    step = 4
    last = h - 1
    threshold = 4
    for y in range(h - 1, -1, -1):
        hit = False
        for x in range(0, w, step):
            px = pixels[x, y]
            if abs(px[0] - bg[0]) > threshold or abs(px[1] - bg[1]) > threshold or abs(px[2] - bg[2]) > threshold:
                hit = True
                break
        if hit:
            last = y
            break
    pad = 18 * SCALE
    bottom = min(h, last + 1 + pad)
    if bottom < h:
        img.crop((0, 0, w, bottom)).save(OUT_PNG)
        logger.info(f"裁剪底部空白：{h} -> {bottom} px")


def main() -> int:
    try:
        df = build_dataframe()
        logger.info(f"共 {len(df)} 条路由，分 {df['group'].nunique()} 组，{COLUMNS} 栏")

        html = HTML_TEMPLATE.format(
            bg=BG,
            logo=LOGO,
            title=TITLE,
            subtitle=SUBTITLE,
            total=len(df),
            columns=build_columns_html(),
            col_count=COLUMNS,
            footer_left=FOOTER_LEFT,
            footer_right=FOOTER_RIGHT,
            width=WIDTH,
        )
        IMG_DIR.mkdir(parents=True, exist_ok=True)
        OUT_HTML.write_text(html, encoding="utf-8")
        logger.info(f"HTML：{OUT_HTML}")

        screenshot()
        crop_bottom()
        logger.success(f"PNG：{OUT_PNG}（{OUT_PNG.stat().st_size / 1024:.0f} KB）")
        return 0
    except Exception:
        logger.error("生成失败：\n" + traceback.format_exc())
        return 1


if __name__ == "__main__":
    sys.exit(main())
