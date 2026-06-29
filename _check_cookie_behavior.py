from streamlit.testing.v1 import AppTest
from streamlit_cookies_manager import EncryptedCookieManager

# Simulate the exact app.py cookie flow
script = """
import streamlit as st
from streamlit_cookies_manager import EncryptedCookieManager

cookies = EncryptedCookieManager(
    prefix="test_app/",
    password="test-secret-key-32-chars-long-enough",
)

st.session_state.setdefault("attempts", 0)

if cookies.ready():
    st.session_state.pop("attempts", None)
    st.success("COOKIES READY")
else:
    st.session_state["attempts"] = st.session_state.get("attempts", 0) + 1
    st.warning(f"COOKIES NOT READY (attempt {st.session_state['attempts']})")
    if st.session_state["attempts"] >= 5:
        st.error("MAX ATTEMPTS")
    else:
        st.rerun()
"""

at = AppTest.from_string(script)

prev_attempts = None
count = 0
while count < 10:
    at.run()
    status = [w.value for w in at.warning if "COOKIES" in str(w.value)] + \
             [s.value for s in at.success if "COOKIES" in str(s.value)]
    print(f"Run {count+1}: {status}", flush=True)
    print(f"  attempts={at.session_state.get('attempts')}", flush=True)
    print(f"  cookies ready={EncryptedCookieManager(prefix='test_app/', password='test-secret-key-32-chars-long-enough').ready()}", flush=True)
    if any("READY" in str(v) for v in status):
        break
    count += 1

print("Total runs:", count+1, flush=True)
