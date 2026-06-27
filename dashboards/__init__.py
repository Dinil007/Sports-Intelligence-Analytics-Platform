"""SPORTA VISTA PRO dashboards package.

Marking this directory as a regular package (PEP 328) instead of relying on
PEP 420 namespace packages. This makes import resolution deterministic under
Streamlit, which inserts the entrypoint script's directory onto sys.path[0]
(see streamlit/web/bootstrap.py::_fix_sys_path) and keeps sys.modules alive
across reruns. Without this file, `dashboards` is a namespace package and the
same source file can be loaded under two distinct module names
(`dashboards.components.*` and top-level `components.*`), which makes
partially-initialized module states much more likely.
"""
