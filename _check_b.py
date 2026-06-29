import os,sys,pathlib
print("PID:",os.getpid())
print("EXE:",sys.executable)
print("CWD:",os.getcwd())
print("PATH[0]:",sys.path[0])
for k in sorted(sys.modules):
    if 'dashboards' in k and ('action_buttons' in k or 'recommendation_card' in k or '4_' in k or 'app' in k):
        m=sys.modules[k]
        print(k, getattr(m,"__file__","NO __file__"), id(m))
