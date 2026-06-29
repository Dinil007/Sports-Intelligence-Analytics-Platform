import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(3)
try:
    s.connect(("localhost", 5432))
    print("PORT_5432_OPEN")
except Exception as e:
    print("PORT_5432_CLOSED", repr(e))
finally:
    s.close()
