#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from icalendar import Calendar, Event
from pathlib import Path

SOURCE_URL = "https://www.officeholidays.com/ics/australia/victoria"

SCRIPT_DIR = Path(__file__).resolve().parent   # = repo 根目錄（檔案就放這）
OUTPUT_DIR = SCRIPT_DIR                         # 直接輸出在根目錄
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
                if k.upper() != "DESCRIPTION":  # 完全移除描述
                    ev.add(k, v)
            clean_cal.add_component(ev)
        elif comp.name not in ("VCALENDAR", "VEVENT"):
            clean_cal.add_component(comp)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)  # 根目錄通常已存在，保險起見
    OUTPUT_PATH.write_bytes(clean_cal.to_ical())

    exists = OUTPUT_PATH.exists() and OUTPUT_PATH.stat().st_size > 0
    size = OUTPUT_PATH.stat().st_size if exists else 0
    print(f"[ok] saved: {OUTPUT_PATH} (exists={exists}, size={size} bytes)")

if __name__ == "__main__":
    main()
