import streamlit as st


ADMIN_QUERY_KEY = "admin"
ADMIN_QUERY_VALUE = "1"
ADMIN_NAV_SESSION_KEY = "admin_nav_enabled"


def hydrate_admin_access() -> bool:
    enabled = bool(st.session_state.get(ADMIN_NAV_SESSION_KEY, False))
    if str(st.query_params.get(ADMIN_QUERY_KEY, "")) == ADMIN_QUERY_VALUE:
        enabled = True
    st.session_state[ADMIN_NAV_SESSION_KEY] = enabled
    return enabled


def admin_nav_enabled() -> bool:
    return bool(st.session_state.get(ADMIN_NAV_SESSION_KEY, False))
