import sys, os, importlib
sys.path.insert(0, '.')
try:
    m = importlib.import_module('streamlit')
    print('STREAMLIT FOUND:', getattr(m, '__file__', 'builtin'))
    print('STREAMLIT VERSION:', getattr(m, '__version__', 'unknown'))
except Exception as e:
    print('IMPORT ERROR:', type(e).__name__, e)
    for p in sys.path:
        candidate = os.path.join(p, 'streamlit')
        if os.path.exists(candidate):
            print('  FOUND dir:', candidate)
        init = os.path.join(candidate, '__init__.py')
        if os.path.exists(init):
            print('  HAS __init__.py:', init)
