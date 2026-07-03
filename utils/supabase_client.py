from supabase import create_client
import streamlit as st


@st.cache_resource
def init_connection():
    return create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])


def get_supabase():
    if "supabase" not in st.session_state:
        st.session_state["supabase"] = init_connection()
    return st.session_state["supabase"]
