"""Test full pitch_dashboard render to find where it stops."""
import sys
from typing import Any

# Mock streamlit with detailed logging
class MockST:
    def __init__(self):
        self.calls = []
    
    def info(self, msg): 
        self.calls.append(f"[info] {msg}")
        print(f"[st.info] {msg}")
    
    def subheader(self, msg): 
        self.calls.append(f"[subheader] {msg}")
        print(f"[st.subheader] {msg}")
    
    def selectbox(self, label, options, **kwargs):
        self.calls.append(f"[selectbox] {label}")
        print(f"[st.selectbox] {label} -> {options[0] if options else 'N/A'}")
        return options[0] if options else None
    
    def container(self): 
        return self
    
    def __enter__(self): 
        return self
    
    def __exit__(self, *args): 
        pass
    
    def divider(self): 
        self.calls.append("[divider]")
        print("-" * 40)
    
    def plotly_chart(self, fig, **kwargs): 
        self.calls.append(f"[plotly_chart] traces={len(fig.data)}, annotations={len(fig._annotations)}")
        print(f"[st.plotly_chart] OK - {len(fig.data)} traces, {len(fig._annotations)} annotations")
        return True

# Mock plotly
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
        pass

class MockGo:
    Figure = MockFigure
    Scatter = MockScatter

sys.modules['streamlit'] = MockST()
sys.modules['plotly'] = type('obj', (object,), {'graph_objects': MockGo()})
sys.modules['plotly.graph_objects'] = MockGo()

# Now test the full pitch_dashboard
from dashboards.components.pitch_visualizations.pitch_dashboard import render_pitch_dashboard
from services.match_intelligence_service import get_match_dashboard

dashboard = get_match_dashboard(4020846)

print("=" * 80)
print("RENDERING FULL PITCH DASHBOARD")
print("=" * 80)

try:
    render_pitch_dashboard(dashboard)
    print("\n" + "=" * 80)
    print("✓ pitch_dashboard COMPLETED SUCCESSFULLY")
    print("=" * 80)
    print("\nAll sections rendered:")
    for call in sys.modules['streamlit'].calls:
        print(f"  {call}")
except Exception as ex:
    import traceback
    print("\n" + "=" * 80)
    print(f"✗ pitch_dashboard FAILED: {type(ex).__name__}: {ex}")
    print("=" * 80)
    traceback.print_exc()
    print("\nCalls made before failure:")
    for call in sys.modules['streamlit'].calls:
        print(f"  {call}")
