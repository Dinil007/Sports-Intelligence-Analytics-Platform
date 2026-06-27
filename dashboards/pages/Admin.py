import sys
from pathlib import Path

# Add project root to Python path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

import streamlit as st

# Auth guard - Admin page requires authentication
from auth.streamlit_auth import is_authenticated
from auth.auth_guard import is_valid_role
if not is_authenticated():
    st.stop()
import pandas as pd
from database.db_connection import engine, SessionLocal
from auth.models import User
from auth.security import get_password_hash

st.title("⚙️ System Administration")
st.markdown("Manage system user database, view session activity, and monitor system settings.")

st.divider()

# Helper function
def get_users_df():
    db = SessionLocal()
    try:
        users = db.query(User).all()
        data = [{
            "ID": u.id,
            "Username": u.username,
            "Email": u.email,
            "Role": u.role.capitalize(),
            "Created At": u.created_at.strftime("%Y-%m-%d %H:%M:%S") if u.created_at else "N/A"
        } for u in users]
        return pd.DataFrame(data)
    finally:
        db.close()

# Layout Columns
col_left, col_right = st.columns([2, 1])

with col_left:
    st.subheader("👥 User Directory")
    try:
        df_users = get_users_df()
        st.dataframe(df_users, use_container_width=True, hide_index=True)
    except Exception as e:
        st.error(f"Error loading user directory: {e}")

with col_right:
    st.subheader("➕ Create New User")
    with st.form("create_user_form", clear_on_submit=True):
        new_username = st.text_input("Username")
        new_email = st.text_input("Email")
        new_password = st.text_input("Password", type="password")
        new_role = st.selectbox("Role", ["admin", "coach", "scout", "analyst"])
        
        submit_btn = st.form_submit_button("Register User", use_container_width=True)
        
        if submit_btn:
            if not new_username or not new_email or not new_password:
                st.error("Please fill in all fields.")
            elif len(new_password) < 6:
                st.error("Password must be at least 6 characters.")
            else:
                db = SessionLocal()
                try:
                    # Check if user already exists
                    dup = db.query(User).filter(
                        (User.username == new_username) | (User.email == new_email)
                    ).first()
                    if dup:
                        st.error("Username or email already exists.")
                    else:
                        hashed = get_password_hash(new_password)
                        u = User(
                            username=new_username,
                            email=new_email,
                            password_hash=hashed,
                            role=new_role
                        )
                        db.add(u)
                        db.commit()
                        st.success(f"Successfully created user '{new_username}' with role '{new_role}'!")
                        st.rerun()
                except Exception as ex:
                    st.error(f"Error creating user: {ex}")
                finally:
                    db.close()

st.divider()

# System Metrics
st.subheader("💻 System Status")
sys_col1, sys_col2, sys_col3 = st.columns(3)

# DB connection status
db_status = "Connected"
try:
    with engine.connect() as conn:
        pass
except Exception:
    db_status = "Disconnected"

sys_col1.metric("Database Status", db_status)
sys_col2.metric("Python Version", sys.version.split(" ")[0])
sys_col3.metric("Streamlit Version", st.__version__)
