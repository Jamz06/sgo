# -*- coding: utf-8 -*-
#!/usr/bin/python
from app import app
#app.run(debug=True, host='0.0.0.0', port=5000)
#app.run(debug=True, host='127.0.0.1', port=5000)
try:
    app.run(host='127.0.0.1', port=5050)
    #app.run(debug=True, host='0.0.0.0', port=5050)
except SystemError:
    exit(0)
