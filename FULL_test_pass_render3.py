"""Full test of render_pass_map with proper mocks to find actual exception."""
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
        print(f"[st.plotly_chart] OK - figure has {len(fig.data)} traces, {len(fig._annotations)} annotations")
        return True

# Mock plotly properly
class MockFigure:
    def __init__(self):
        self.data = []
        self.layout = {}
        self._shapes = []
        self._annotations = []
    
    def add_trace(self, trace):
        self.data.append(trace)
        return self
    
    def add_shape(self, **kwargs):
        self._shapes.append(kwargs)
        return self
    
    def add_annotation(self, **kwargs):
        self._annotations.append(kwargs)
        return self
    
    def update_layout(self, **kwargs):
        self.layout.update(kwargs)
        return self
    
    def update_xaxes(self, **kwargs):
        return self
    
    def update_yaxes(self, **kwargs):
        return self

class MockScatter:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

class MockGo:
    Figure = MockFigure
    Scatter = MockScatter

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
    print(f"✓ render_pitch() OK - {len(fig._shapes)} shapes")
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
print("STEP 3: Test ALL subsequent maps after pass_map")
print("=" * 80)
try:
    from dashboards.components.pitch_visualizations.carry_map import render_carry_map
    render_carry_map(events)
    print("✓ render_carry_map() COMPLETED SUCCESSFULLY")
except Exception as ex:
    import traceback
    print(f"✗ FAILED at carry_map: {type(ex).__name__}: {ex}")
    traceback.print_exc()

try:
    from dashboards.components.pitch_visualizations.pressure_map import render_pressure_map  
    render_pressure_map(events)
    print("✓ render_pressure_map() COMPLETED SUCCESSFULLY")
except Exception as ex:
    import traceback
    print(f"✗ FAILED at pressure_map: {type(ex).__name__}: {ex}")
    traceback.print_exc()

try:
    from dashboards.components.pitch_visualizations.defensive_actions_map import render_defensive_actions
    render_defensive_actions(events)
    print("✓ render_defensive_actions() COMPLETED SUCCESSFULLY")
except Exception as ex:
    import traceback
    print(f"✗ FAILED at defensive_actions: {type(ex).__name__}: {ex}")
    traceback.print_exc()
