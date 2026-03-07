"""
items.html のダガーセクションからアイテムデータを CSV に抽出するスクリプト。
"""

import csv
from pathlib import Path

from bs4 import BeautifulSoup

# プロジェクトルート: src/data_spoiler/ から4階層上
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
INPUT_HTML   = PROJECT_ROOT / "data" / "base" / "items.html"
OUTPUT_CSV   = PROJECT_ROOT / "data" / "temp" / "dagger.csv"


def extract_dagger(input_html: Path, output_csv: Path) -> int:
    """ダガーテーブルを解析して CSV に書き出す。件数を返す。"""

    with input_html.open(encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    # id="dagger" の anchor を起点にテーブルを探す
    anchor = soup.find(id="dagger")
    table  = anchor.find_next("table", class_="style_table")

    records = []
    for tr in table.tbody.find_all("tr"):
        tds = tr.find_all("td")
        if len(tds) < 7:
            continue

        name      = tds[0].get_text(strip=True)
        rank      = tds[1].get_text(strip=True)
        drop      = tds[2].get_text(separator=" ", strip=True)

        # 属性: <img> の title 属性
        img = tds[3].find("img")
        attribute = img["title"] if img else ""

        stats     = tds[4].get_text(separator=" ", strip=True)
        skill     = tds[5].get_text(separator=" ", strip=True)
        note      = tds[6].get_text(separator=" ", strip=True)

        records.append([name, rank, drop, attribute, stats, skill, note])

    output_csv.parent.mkdir(parents=True, exist_ok=True)
    with output_csv.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["名称", "ランク", "ドロップ", "属性", "基本性能", "スキル", "備考"])
        writer.writerows(records)

    return len(records)


def main() -> None:
    count = extract_dagger(INPUT_HTML, OUTPUT_CSV)
    print(f"抽出完了: {count} 件 → {OUTPUT_CSV}")
