import pathlib
p = pathlib.Path(r"d:\Sports Intelligence & Analytics Platform\dashboards\components\recommendation_card.py")
data = p.read_bytes()
start = data.find(b"def render_recommendation_card")
print(repr(data[start:start+700]))
