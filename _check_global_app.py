import sys, runpy, os, pathlib

os.chdir(r'D:\Sports Intelligence & Analytics Platform')
code = pathlib.Path(r'D:\Sports Intelligence & Analytics Platform\dashboards\app.py').read_text()
# Preflight: try to import dashboards.app with global python to see where it loads from
sys.path.insert(0, r'D:\Sports Intelligence & Analytics Platform')
try:
    import dashboards.app as appmod
    print('dashboards.app loaded from:', getattr(appmod, '__file__', None))
except Exception as e:
    print('IMPORT ERROR:', repr(e))

# show streamlit version if available
try:
    import streamlit
    print('streamlit:', streamlit.__file__)
    print('streamlit version:', streamlit.__version__)
except Exception as e:
    print('streamlit not imported:', repr(e))
