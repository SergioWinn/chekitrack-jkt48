import re

import streamlit as st
from supabase import create_client


AUTH_CLIENT_SESSION_KEY = "auth_supabase"
AUTH_SESSION_STORAGE_KEY = "auth_session"
AUTH_USER_STORAGE_KEY = "auth_user"
AUTH_PROFILE_STORAGE_KEY = "auth_profile"
AUTH_EMAIL_DOMAIN = "users.chekitrack.local"


def normalize_username(username: str) -> str:
    return (username or "").strip().lower()


def validate_username(username: str) -> str | None:
    normalized = normalize_username(username)
    if not re.fullmatch(r"[a-z0-9](?:[a-z0-9._-]{1,28}[a-z0-9])?", normalized):
        return "Use 3-30 characters: lowercase letters, numbers, dot, underscore, or hyphen."
    return None


def username_to_email(username: str) -> str:
    return f"{normalize_username(username)}@{AUTH_EMAIL_DOMAIN}"


def get_auth_client():
    if AUTH_CLIENT_SESSION_KEY not in st.session_state:
        st.session_state[AUTH_CLIENT_SESSION_KEY] = create_client(
            st.secrets["SUPABASE_URL"],
            st.secrets["SUPABASE_KEY"],
        )
    return st.session_state[AUTH_CLIENT_SESSION_KEY]


def clear_auth_state():
    for key in [
        AUTH_SESSION_STORAGE_KEY,
        AUTH_USER_STORAGE_KEY,
        AUTH_PROFILE_STORAGE_KEY,
        "admin_authenticated",
    ]:
        st.session_state.pop(key, None)


def _store_auth_response(response):
    session = getattr(response, "session", None)
    user = getattr(response, "user", None)
    if session is None or user is None:
        clear_auth_state()
        return False

    st.session_state[AUTH_SESSION_STORAGE_KEY] = {
        "access_token": session.access_token,
        "refresh_token": session.refresh_token,
    }
    st.session_state[AUTH_USER_STORAGE_KEY] = user
    return True


def fetch_current_profile():
    user = current_user()
    if user is None:
        st.session_state.pop(AUTH_PROFILE_STORAGE_KEY, None)
        return None

    response = (
        get_auth_client()
        .table("profiles")
        .select("id, username, role, created_at")
        .eq("id", user.id)
        .limit(1)
        .execute()
    )
    rows = response.data or []
    profile = rows[0] if rows else None
    st.session_state[AUTH_PROFILE_STORAGE_KEY] = profile
    return profile


def hydrate_auth_session() -> bool:
    tokens = st.session_state.get(AUTH_SESSION_STORAGE_KEY)
    if not tokens:
        return False

    try:
        response = get_auth_client().auth.set_session(
            tokens["access_token"],
            tokens["refresh_token"],
        )
    except Exception:
        clear_auth_state()
        return False

    if not _store_auth_response(response):
        return False

    fetch_current_profile()
    return True


def current_user():
    return st.session_state.get(AUTH_USER_STORAGE_KEY)


def current_profile():
    return st.session_state.get(AUTH_PROFILE_STORAGE_KEY)


def current_username() -> str | None:
    profile = current_profile()
    if profile:
        return profile.get("username")
    user = current_user()
    if user:
        return normalize_username((user.email or "").split("@", 1)[0])
    return None


def is_authenticated() -> bool:
    return current_user() is not None


def is_admin() -> bool:
    profile = current_profile()
    return bool(profile and profile.get("role") == "admin")


def sign_up_with_username(username: str, password: str):
    username_error = validate_username(username)
    if username_error:
        return False, username_error
    if len(password or "") < 8:
        return False, "Use at least 8 characters for the password."

    try:
        response = get_auth_client().auth.sign_up(
            {
                "email": username_to_email(username),
                "password": password,
            }
        )
    except Exception as exc:
        return False, str(exc)

    if not _store_auth_response(response):
        return (
            False,
            "Sign-up did not return a login session. Disable email confirmation in Supabase Auth for this username-first flow.",
        )

    user = current_user()
    try:
        get_auth_client().table("profiles").insert(
            {
                "id": user.id,
                "username": normalize_username(username),
            }
        ).execute()
    except Exception as exc:
        clear_auth_state()
        return False, str(exc)

    fetch_current_profile()
    return True, "Account created."


def sign_in_with_username(username: str, password: str):
    username_error = validate_username(username)
    if username_error:
        return False, username_error

    try:
        response = get_auth_client().auth.sign_in_with_password(
            {
                "email": username_to_email(username),
                "password": password,
            }
        )
    except Exception as exc:
        return False, str(exc)

    if not _store_auth_response(response):
        return False, "Login failed."

    fetch_current_profile()
    return True, "Signed in."


def sign_out_user():
    try:
        get_auth_client().auth.sign_out()
    except Exception:
        pass
    clear_auth_state()
