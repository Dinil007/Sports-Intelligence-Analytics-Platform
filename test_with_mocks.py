"""Test render_pass_map with full mocks."""
import sys

# Mock both streamlit and plotly before importing
class MockFigure:
    def __init__(self):
        self.data = []
        self.layout = {}
    def add_trace(self, trace):
        self.data.append(trace)
        return self
    def update_layout(self, **kwargs):
        self.layout.update(kwargs)
        return self
    def add_annotation(self, **kwargs):
        # This is where the issue might be
        pass

class MockGo:
    Figure = MockFigure
    Scatter = lambda **kw: kw

class MockST:
    def info(self, msg): pass
    def subheader(self, msg): pass
    def container(self): 
        return self
    def __enter__(self): return self
    def __exit__(self, *args): pass
    def divider(self): pass
    def plotly_chart(self, fig, **kwargs): 
        return True

sys.modules['streamlit'] = MockST()
sys.modules['plotly'] = type('obj', (object,), {'graph_objects': MockGo()})
sys.modules['plotly.graph_objects'] = MockGo()

# Now import the module
from dashboards.components.pitch_visualizations.pass_map import render_pass_map
from services.match_intelligence_service import get_match_dashboard

dashboard = get_match_dashboard(4020846)
events = dashboard.get("events", [])

print("Attempting to render_pass_map...")
try:
    render_pass_map(events)
    print("SUCCESS: render_pass_map completed")
except Exception as ex:
    import traceback
    print(f"FAILED: {type(ex).__name__}: {ex}")
    traceback.print_exc()
