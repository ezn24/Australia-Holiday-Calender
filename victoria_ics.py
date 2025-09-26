#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from icalendar import Calendar
from pathlib import Path

SOURCE_URL = "https://www.officeholidays.com/ics/australia/victoria"

OUT = Path(__file__).resolve().parent / "victoria.cleaned.ics"

def main():
    r = requests.get(SOURCE_URL, timeout=60)
    r.raise_for_status()

    cal = Calendar.from_ical(r.content)

    # 就地移除 DESCRIPTION / X-ALT-DESC（部分來源會提供 HTML 版）
    for vevent in cal.walk("VEVENT"):
        vevent.pop("DESCRIPTION", None)
        vevent.pop("X-ALT-DESC", None)

    OUT.write_bytes(cal.to_ical())
    print(f"[ok] wrote {OUT} ({OUT.stat().st_size} bytes)")

if __name__ == "__main__":
    main()
