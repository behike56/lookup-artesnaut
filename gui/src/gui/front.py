import json
import pathlib

import pandas as pd
import streamlit as st

DATA_DIR = pathlib.Path(__file__).parents[3] / "data" / "items"


def base_settings() -> None:
    st.set_page_config(page_title="アルテスノート アイテム一覧", layout="wide")
    st.title("アルテスノート アイテム一覧")

    tab_weapon, tab_armor, tab_accessory, tab_shield = st.tabs(["武器", "防具", "アクセサリ", "盾"])

    with tab_weapon:
        st.dataframe(_load_items("weapon.json"), use_container_width=True)

    with tab_armor:
        st.dataframe(_load_items("armor.json"), use_container_width=True)

    with tab_accessory:
        st.dataframe(_load_items("accessory.json"), use_container_width=True)

    with tab_shield:
        st.dataframe(_load_items("shield.json"), use_container_width=True)


def _load_items(filename: str) -> pd.DataFrame:
    with open(DATA_DIR / filename) as f:
        items = json.load(f)
    rows = []
    for item in items:
        row = {k: v for k, v in item.items() if k != "basics"}
        row.update(item.get("basics", {}))
        rows.append(row)
    return pd.DataFrame(rows)
