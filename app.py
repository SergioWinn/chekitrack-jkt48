import streamlit as st
from utils.admin_access import hydrate_admin_access
from utils.styles import DARK_THEME_CSS
from utils.supabase_client import get_supabase

st.set_page_config(
    page_title="Chekicha Timeline",
    page_icon="📸",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(DARK_THEME_CSS, unsafe_allow_html=True)

get_supabase()
hydrate_admin_access()

st.switch_page("pages/1_📊_Overview.py")
