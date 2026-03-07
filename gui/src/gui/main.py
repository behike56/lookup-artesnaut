import json
import pathlib

import pandas as pd
import streamlit as st

DATA_DIR = pathlib.Path(__file__).parents[3] / "data" / "items"

st.set_page_config(page_title="アルテスノート アイテム一覧", layout="wide")
st.title("アルテスノート アイテム一覧")


def load_items(filename):
    with open(DATA_DIR / filename) as f:
        items = json.load(f)
    rows = []
    for item in items:
        row = {k: v for k, v in item.items() if k != "basics"}
        row.update(item.get("basics", {}))
        rows.append(row)
    return pd.DataFrame(rows)


tab_weapon, tab_armor, tab_accessory, tab_shield = st.tabs(["武器", "防具", "アクセサリ", "盾"])

with tab_weapon:
    df = load_items("weapon.json")
    st.dataframe(df, use_container_width=True)

with tab_armor:
    df = load_items("armor.json")
    st.dataframe(df, use_container_width=True)

with tab_accessory:
    df = load_items("accessory.json")
    st.dataframe(df, use_container_width=True)

with tab_shield:
    df = load_items("shield.json")
    st.dataframe(df, use_container_width=True)
