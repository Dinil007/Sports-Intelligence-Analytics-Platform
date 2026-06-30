"""Test if Streamlit rendering causes the issue."""
import sys
sys.path.insert(0, '.')

# Mock streamlit to avoid needing the module
class MockST:
    def info(self, msg): print(f"[st.info] {msg}")
    def subheader(self, msg): print(f"[st.subheader] {msg}")
    def container(self): return self
    def __enter__(self): return self
    def __exit__(self, *args): pass
    def divider(self): print("-" * 40)
    def plotly_chart(self, fig, **kwargs): 
        print(f"[st.plotly_chart] rendered chart with {len(fig.data)} traces")
        return True

sys.modules['streamlit'] = MockST()

# Now try importing and running
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
