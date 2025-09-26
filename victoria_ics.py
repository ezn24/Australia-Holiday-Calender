#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from icalendar import Calendar, Event
from pathlib import Path

SOURCE_URL = "https://www.officeholidays.com/ics/australia/victoria"

# 以腳本檔所在目錄為基準，輸出到 ../dist/victoria.cleaned.ics（也可改成同層 dist）
SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = (SCRIPT_DIR / "")       # 想放 repo 根目錄就改成 SCRIPT_DIR.parent / "dist"
OUTPUT_PATH = OUTPUT_DIR / "victoria.cleaned.ics"

def main():
    print(f"[info] script_dir={SCRIPT_DIR}")
    print(f"[info] will write to: {OUTPUT_PATH}")

    resp = requests.get(SOURCE_URL, timeout=60)
    resp.raise_for_status()

    cal = Calendar.from_ical(resp.content)

    clean_cal = Calendar()
    for k, v in cal.property_items():
        clean_cal.add(k, v)

    for comp in cal.walk():
        if comp.name == "VEVENT":
            ev = Event()
            for k, v in comp.property_items():
                if k.upper() != "DESCRIPTION":  # 直接略過描述
                    ev.add(k, v)
            clean_cal.add_component(ev)
        elif comp.name not in ("VCALENDAR", "VEVENT"):
            clean_cal.add_component(comp)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_bytes(clean_cal.to_ical())

    # 立即確認
    exists = OUTPUT_PATH.exists() and OUTPUT_PATH.stat().st_size > 0
    print(f"[ok] saved: {OUTPUT_PATH} (exists={exists}, size={OUTPUT_PATH.stat().st_size if exists else 0} bytes)")

if __name__ == "__main__":
    main()
