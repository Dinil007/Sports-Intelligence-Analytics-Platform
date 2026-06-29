with open(r"d:\Sports Intelligence & Analytics Platform\dashboards\components\recommendation_card.py", "rb") as f:
    data = f.read()
start = data.find(b"def render_recommendation_card")
print(repr(data[start:start+500]))
