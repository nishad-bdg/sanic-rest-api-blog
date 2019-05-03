from sanic import Sanic
from sanic.response import json
from sanic import Blueprint

app = Sanic('test')

@app.route('/')
async def home(request):
    return json({'hello':'World'})


if __name__ == "__main__":
    app.run(debug = True)
