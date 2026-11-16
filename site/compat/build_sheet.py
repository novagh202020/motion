"""App connection-log export -> the compatibility sheet the checker page reads.

Keeps only برند / مدل / سال ساخت / وضعیت (no phone numbers, no device IDs), one row per
model+year. Writes UTF-8 with BOM so Excel opens the Persian text correctly.

    python3 build_sheet.py connection_logs.csv            # -> cardiag-compat.csv next to this file
"""
import csv, sys, pathlib

src = sys.argv[1]
out = pathlib.Path(sys.argv[2]) if len(sys.argv) > 2 else pathlib.Path(__file__).with_name("cardiag-compat.csv")

rows = {}
with open(src, encoding="utf-8-sig", newline="") as f:
    for r in csv.DictReader(f):
        brand, model, year = r["برند"].strip(), r["مدل"].strip(), r["سال"].strip()
        if not (brand and model and year):
            continue
        ok = r["وضعیت"].strip() == "موفق"
        key = (brand, model, year)
        rows[key] = rows.get(key, False) or ok

with open(out, "w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f)
    w.writerow(["برند", "مدل", "سال ساخت", "وضعیت"])
    for (b, m, y), ok in sorted(rows.items()):
        w.writerow([b, m, y, "موفق" if ok else "ناموفق"])
print(f"{len(rows)} rows -> {out}")
