import pathlib

path = pathlib.Path(r"d:\Sports Intelligence & Analytics Platform\dashboards\pages\4_🔄_Transfer_Recommendations.py")
text = path.read_text(encoding="utf-8")

needle = '        for rec in st.session_state.recommendations:\r\n            render_recommendation_card(rec)'
insert = '        import traceback\r\n\r\n        st.write("ENTER LOOP")\r\n        st.code("".join(traceback.format_stack(limit=20)))\r\n\r\n        for rec in st.session_state.recommendations:\r\n            render_recommendation_card(rec)'

if needle in text:
    text = text.replace(needle, insert, 1)
    path.write_text(text, encoding="utf-8")
    print("PATCHED")
else:
    raw = path.read_bytes()
    b_needle = needle.encode("utf-8")
    if b_needle in raw:
        raw = raw.replace(b_needle, insert.encode("utf-8"), 1)
        path.write_bytes(raw)
        print("PATCHED (bytes fallback)")
    else:
        print("NEEDLE NOT FOUND")
        print(repr(text[5000:5500]))
