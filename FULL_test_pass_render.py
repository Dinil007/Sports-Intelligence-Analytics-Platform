"""Full test of render_pass_map with mocks to find actual exception."""
import sys
from typing import Any

# Mock streamlit
class MockST:
    def info(self, msg): print(f"[st.info] {msg}")
    def subheader(self, msg): print(f"[st.subheader] {msg}")
    def container(self): 
        return self
    def __enter__(self): return self
    def __exit__(self, *args): pass
    def divider(self): print("-" * 40)
    def plotly_chart(self, fig, **kwargs): 
        print(f"[st.plotly_chart] OK - figure has {len(fig.data)} traces")
        return True

# Mock plotly
class MockAnnotation:
    def __init__(self, **kwargs):
        pass

class MockFigure:
    def __init__(self):
        self.data = []
        self.layout = {}
        self.annotations = []
    def add_trace(self, trace):
        self.data.append(trace)
        return self
    def add_annotation(self, **kwargs):
        self.annotations.append(kwargs)
        return self
    def update_layout(self, **kwargs):
        self.layout.update(kwargs)
        return self

class MockGo:
    Figure = MockFigure
    Scatter = lambda **kw: {"type": "scatter", **kw}

sys.modules['streamlit'] = MockST()
sys.modules['plotly'] = type('obj', (object,), {'graph_objects': MockGo()})
sys.modules['plotly.graph_objects'] = MockGo()

# Now import and test
from dashboards.components.pitch_visualizations.football_pitch import render_pitch
from dashboards.components.pitch_visualizations.pass_map import render_pass_map
from services.match_intelligence_service import get_match_dashboard

dashboard = get_match_dashboard(4020846)
events = dashboard.get("events", [])

print("=" * 80)
print("STEP 1: Test render_pitch()")
print("=" * 80)
try:
    fig = render_pitch()
    print(f"✓ render_pitch() OK - created figure with {len(fig.annotations)} annotations/shapes")
except Exception as ex:
    import traceback
    print(f"✗ FAILED: {type(ex).__name__}: {ex}")
    traceback.print_exc()

print("\n" + "=" * 80)
print("STEP 2: Test render_pass_map()")
print("=" * 80)
try:
    render_pass_map(events)
    print("✓ render_pass_map() COMPLETED SUCCESSFULLY")
except Exception as ex:
    import traceback
    print(f"✗ FAILED: {type(ex).__name__}: {ex}")
    traceback.print_exc()

print("\n" + "=" * 80)
print("STEP 3: Test carry_map after pass_map")
print("=" * 80)
try:
    from dashboards.components.pitch_visualizations.carry_map import render_carry_map
    render_carry_map(events)
    print("✓ render_carry_map() COMPLETED SUCCESSFULLY")
except Exception as ex:
    import traceback
    print(f"✗ FAILED: {type(ex).__name__}: {ex}")
    traceback.print_exc()
