"""
data/temp/ の CSV ファイルを items の形式に変換するスクリプト。

出力: data/items/{group_key}.json（グループごとに分割）
  weapon.json    → [ { weap_id, name, category, rank, attribute, basics, skill, set, drop }, ... ]
  shield.json    → [ ... ]
  armor.json     → [ ... ]
  accessory.json → [ ... ]
"""

import csv
import json
import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
CSV_DIR      = PROJECT_ROOT / "data" / "temp"
OUTPUT_DIR   = PROJECT_ROOT / "data" / "items"

# top-level キー → [(anchor_id, カテゴリ表示名), ...]
CATEGORY_GROUPS: dict[str, list[tuple[str, str]]] = {
    "weapon": [
        ("dagger",     "短剣"),
        ("sword",      "片手剣"),
        ("blade",      "大剣"),
        ("lance",      "槍"),
        ("axe",        "斧"),
        ("knuckle",    "拳"),
        ("bow",        "弓"),
        ("staff",      "杖"),
        ("gun",        "銃"),
    ],
    "shield": [
        ("shield",     "盾"),
    ],
    "armor": [
        ("helmet",     "頭"),
        ("lightArmor", "軽鎧"),
        ("heavyArmor", "重鎧"),
        ("arms",       "手"),
        ("boots",      "脚"),
    ],
    "accessory": [
        ("necklace",   "ネックレス"),
        ("mantle",     "マント"),
        ("ring",       "指輪"),
        ("belt",       "ベルト"),
        ("jewel",      "宝石"),
        ("bottle",     "瓶"),
        ("other",      "その他"),
    ],
}


def parse_basics(s: str) -> dict[str, int | float]:
    """'攻撃力：20 攻撃回数：3 致命打率：10.0 ...' → {'攻撃力': 20, ...}"""
    if not s:
        return {}
    result = {}
    for key, val in re.findall(r'([^：\s]+)：(-?[\d.]+)', s):
        result[key] = float(val) if '.' in val else int(val)
    return result


def parse_skills(s: str) -> list[str]:
    """スキル文字列をリストに分割する。"""
    if not s:
        return []
    return [t for t in s.split(" ") if t]


def parse_set(note: str) -> list[str]:
    """備考から 'XXXセット' を抽出する。"""
    return re.findall(r'\S+セット', note)


def load_csv(anchor_id: str) -> list[dict[str, str]]:
    path = CSV_DIR / f"{anchor_id}.csv"
    if not path.exists():
        print(f"  [WARN] {path.name} が見つかりません")
        return []
    with path.open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


def convert_row(row: dict[str, str], category: str, weap_id: int) -> dict:
    return {
        "weap_id":   weap_id,
        "name":      row["名称"],
        "category":  category,
        "rank":      row["ランク"],
        "attribute": row["属性"],
        "basics":    parse_basics(row["基本性能"]),
        "skill":     parse_skills(row["スキル"]),
        "set":       parse_set(row["備考"]),
        "drop": {
            "location": row["ドロップ"].split(),
            "monster":  "",
        },
    }


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    weap_id = 1
    total = 0

    for group_key, sections in CATEGORY_GROUPS.items():
        items = []
        for anchor_id, category in sections:
            rows = load_csv(anchor_id)
            for row in rows:
                items.append(convert_row(row, category, weap_id))
                weap_id += 1

        out_path = OUTPUT_DIR / f"{group_key}.json"
        with out_path.open("w", encoding="utf-8") as f:
            json.dump(items, f, ensure_ascii=False, indent=2)

        total += len(items)
        print(f"  {group_key:10s}: {len(items):4d} 件 → {out_path.name}")

    print(f"\n完了: 合計 {total} 件 → {OUTPUT_DIR}/")
