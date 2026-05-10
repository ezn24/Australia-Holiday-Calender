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

    for vevent in cal.walk("VEVENT"):
        vevent.pop("DESCRIPTION", None)
        vevent.pop("X-ALT-DESC", None)

    new_data = cal.to_ical()

    if OUT.exists() and OUT.read_bytes() == new_data:
        print("[ok] no content changes")
        return

    OUT.write_bytes(new_data)
    print(f"[ok] wrote {OUT} ({len(new_data)} bytes)")

if __name__ == "__main__":
    main()
