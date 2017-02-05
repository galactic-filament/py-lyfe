from app import app
import os

app.debug = True
app.run(host='0.0.0.0', port=os.environ['APP_PORT'])
