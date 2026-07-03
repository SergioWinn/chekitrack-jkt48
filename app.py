import streamlit as st
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

st.switch_page("pages/1_📊_Overview.py")
