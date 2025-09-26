#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import requests
from icalendar import Calendar, Event

SOURCE_URL = "https://www.officeholidays.com/ics/australia/victoria"
OUTPUT_PATH = "victoria.cleaned.ics"

# 在這裡自訂要刪除的內容（順序會依序套用）
# 可放純字串或正則（用 raw string）。以下是範例，請按你的需求調整：
REMOVE_PATTERNS = [
    r"\s*Visit\s+officeholidays\.com.*$",          # 刪官方宣傳尾巴
    r"\s*See\s+more\s+at\s+.*$",                   # 刪多餘連結
    r"\s*Public\s+Holiday\s*$",                    # 刪字尾 "Public Holiday"
    r"\s*\(observed\)\s*$",                        # 刪 "(observed)"
]

def clean_description(text: str) -> str:
    if not text:
        return text
    # iCal 內常出現跳行與 escaped 字元，requests 取回後 icalendar 會處理解折行
    desc = str(text)
    for pat in REMOVE_PATTERNS:
        desc = re.sub(pat, "", desc, flags=re.IGNORECASE | re.MULTILINE)
    # 也可順手做 trim 與多空白壓縮
    desc = re.sub(r"[ \t]+", " ", desc).strip()
    return desc

def main():
    # 下載 ICS 原檔
    resp = requests.get(SOURCE_URL, timeout=60)
    resp.raise_for_status()
    raw = resp.content

    cal = Calendar.from_ical(raw)

    # 新建一份乾淨的行事曆，保留原來屬性（PRODID、VERSION…）
    clean_cal = Calendar()
    for k, v in cal.property_items():
        clean_cal.add(k, v)

    for comp in cal.walk():
        if comp.name == "VEVENT":
            ev = Event()
            # 複製所有屬性
            for k, v in comp.property_items():
                if k.upper() == "DESCRIPTION":
                    ev.add("DESCRIPTION", clean_description(v))
                else:
                    ev.add(k, v)
            clean_cal.add_component(ev)
        elif comp.name not in ("VCALENDAR", "VEVENT"):
            # 其他元件（如 VTIMEZONE）照抄
            clean_cal.add_component(comp)

    # 寫檔
    import os
    os.makedirs("dist", exist_ok=True)
    with open(OUTPUT_PATH, "wb") as f:
        f.write(clean_cal.to_ical())

if __name__ == "__main__":
    main()
