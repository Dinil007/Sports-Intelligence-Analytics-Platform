import pathlib

path = pathlib.Path(r"d:\Sports Intelligence & Analytics Platform\dashboards\components\recommendation_card.py")
text = path.read_text(encoding="utf-8")

needle = '    """\r\n    name = player.get("player_name", "Unknown")'
insert = '    """\r\n    import traceback\r\n\r\n    st.code(\r\n        "".join(traceback.format_stack(limit=25)),\r\n        language="text",\r\n    )\r\n\r\n    name = player.get("player_name", "Unknown")'

if needle in text:
    text = text.replace(needle, insert, 1)
    path.write_text(text, encoding="utf-8")
    print("PATCHED")
else:
    # fallback: raw bytes search
    raw = path.read_bytes()
    b_needle = b'    """\r\n    name = player.get("player_name", "Unknown")'
    if b_needle in raw:
        raw = raw.replace(b_needle, insert.encode("utf-8"), 1)
        path.write_bytes(raw)
        print("PATCHED (bytes fallback)")
    else:
        print("NEEDLE NOT FOUND")
