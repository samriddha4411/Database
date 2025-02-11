from app import *

import socket

print(socket.gethostname())
print(socket.gethostbyname(socket.gethostname()))

app.run(debug=True, host=socket.gethostbyname(socket.gethostname()), port=80)