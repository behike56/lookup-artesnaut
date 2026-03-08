"""
items.html の各アイテムカテゴリからデータを CSV に抽出するスクリプト。
"""

import csv
from pathlib import Path

from bs4 import BeautifulSoup

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
INPUT_HTML   = PROJECT_ROOT / "data" / "base" / "items.html"
OUTPUT_DIR   = PROJECT_ROOT / "data" / "temp"

# anchor id → 出力ファイル名（アイテム種別一覧）
# weapon / armor / accessory は親セクション（テーブルなし）のためスキップ
SECTIONS: list[tuple[str, str]] = [
    ("dagger",     "短剣"),
    ("sword",      "片手剣"),
    ("blade",      "大剣"),
    ("lance",      "槍"),
    ("axe",        "斧"),
    ("knuckle",    "拳"),
    ("bow",        "弓"),
    ("staff",      "杖"),
    ("gun",        "銃"),
    ("shield",     "盾"),
    ("helmet",     "頭"),
    ("lightArmor", "軽鎧"),
    ("heavyArmor", "重鎧"),
    ("arms",       "手"),
    ("boots",      "脚"),
    ("necklace",   "ネックレス"),
    ("mantle",     "マント"),
    ("ring",       "指輪"),
    ("belt",       "ベルト"),
    ("jewel",      "宝石"),
    ("bottle",     "瓶"),
    ("other",      "その他"),
]

HEADER = ["名称", "ランク", "ドロップ", "属性", "基本性能", "スキル", "備考"]


def extract_section(soup: BeautifulSoup, anchor_id: str) -> list[list[str]]:
    """anchor_id に対応するテーブルの全行を抽出して返す。"""
    anchor = soup.find(id=anchor_id)
    if anchor is None:
        raise ValueError(f"anchor id='{anchor_id}' not found")

    table = anchor.find_next("table", class_="style_table")
    if table is None or table.tbody is None:
        raise ValueError(f"table not found after id='{anchor_id}'")

    records = []
    for tr in table.tbody.find_all("tr"):
        tds = tr.find_all("td")
        if len(tds) < 7:
            continue

        name      = tds[0].get_text(strip=True)
        rank      = tds[1].get_text(strip=True)
        drop      = tds[2].get_text(separator=" ", strip=True)

        img       = tds[3].find("img")
        attribute = img["title"] if img else ""

        stats     = tds[4].get_text(separator=" ", strip=True)
        skill     = tds[5].get_text(separator=" ", strip=True)
        note      = tds[6].get_text(separator=" ", strip=True)

        records.append([name, rank, drop, attribute, stats, skill, note])

    return records


def main() -> None:
    print(f"読み込み中: {INPUT_HTML}")
    with INPUT_HTML.open(encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for anchor_id, label in SECTIONS:
        try:
            records = extract_section(soup, anchor_id)
        except ValueError as e:
            print(f"  [SKIP] {e}")
            continue

        out_path = OUTPUT_DIR / f"{anchor_id}.csv"
        with out_path.open("w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(HEADER)
            writer.writerows(records)

        print(f"  {label:8s} ({anchor_id:10s}): {len(records):3d} 件 → {out_path.name}")

    print("完了")
