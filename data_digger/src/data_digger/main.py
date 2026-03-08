import csv
import re

import pandas as pd
import requests
from bs4 import BeautifulSoup

URL = (
    "https://artesnaut.com/wiki/?%E3%82%A2%E3%82%A4%E3%83%86%E3%83%A0%E5%9B%B3%E9%91%91"
)
OUTPUT_CSV = "output/items.csv"

# 抽出対象カラム（ページのヘッダー名に合わせて調整してください）
TARGET_COLUMNS = ["名称", "ランク", "ドロップ", "属性", "基本性能", "スキル", "備考"]


def fetch_page(url: str) -> BeautifulSoup:
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers, timeout=10)
    response.encoding = "utf-8"
    return BeautifulSoup(response.text, "html.parser")


def find_target_table(soup: BeautifulSoup) -> list:
    """
    ページ内のテーブルを走査し、TARGET_COLUMNSを含むテーブルを抽出する。
    """
    tables = soup.find_all("table")
    print(f"テーブル数: {len(tables)}")

    for i, table in enumerate(tables):
        # ヘッダー行を取得
        headers = []
        header_row = table.find("tr")
        if not header_row:
            continue

        for th in header_row.find_all(["th", "td"]):
            headers.append(th.get_text(strip=True))

        print(f"Table[{i}] ヘッダー: {headers}")

        # TARGET_COLUMNSがどれか1つでも含まれていればそのテーブルを対象とする
        if not any(col in headers for col in TARGET_COLUMNS):
            continue

        print(f"-> 対象テーブルを発見: Table[{i}]")
        return extract_rows(table, headers)

    print("対象テーブルが見つかりませんでした。")
    return []


def extract_rows(table, headers: list) -> list:
    rows_data = []
    rows = table.find_all("tr")[1:]  # ヘッダー行をスキップ

    for row in rows:
        cells = row.find_all(["td", "th"])
        if not cells:
            continue

        row_dict = {}
        for j, cell in enumerate(cells):
            if j < len(headers):
                col_name = headers[j]
                # TARGET_COLUMNSに含まれるカラムのみ抽出
                if col_name in TARGET_COLUMNS:
                    if col_name == "属性":
                        titles = [a["title"] for a in cell.find_all("a", title=True)]
                        text = " ".join(titles)
                    else:
                        text = cell.get_text(separator=" ", strip=True)
                        text = re.sub(r"\s+", " ", text).strip()
                    row_dict[col_name] = text

        if row_dict:
            rows_data.append(row_dict)

    return rows_data


def save_csv(data: list, output_path: str):
    if not data:
        print("データが空のため、CSVを出力しません。")
        return

    # TARGET_COLUMNSの順序でカラムを並べる（存在するもののみ）
    fieldnames = [col for col in TARGET_COLUMNS if col in data[0]]

    with open(output_path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(data)

    print(f"CSV出力完了: {output_path} ({len(data)}件)")


def main():
    print(f"取得中: {URL}")
    soup = fetch_page(URL)

    data = find_target_table(soup)

    if data:
        # 先頭3件をプレビュー表示
        df = pd.DataFrame(data)
        print("\n--- プレビュー (先頭3件) ---")
        print(df.head(3).to_string(index=False))
        print()

        save_csv(data, OUTPUT_CSV)
    else:
        print(
            "\nヒント: TARGET_COLUMNS をページ実際のヘッダー名に合わせて修正してください。"
        )


if __name__ == "__main__":
    main()
