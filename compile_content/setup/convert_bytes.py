import os

# convert app.zip as "app" files in bytes
with open("app.zip", "rb") as f:
    data = f.read()

# create app.bytes
with open("app", "wb") as f:
    f.write(data)
