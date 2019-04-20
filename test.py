from sanic import Sanic
from sanic.log import logger 
from sanic.response import text

app = Sanic('test')

@app.route('/')
async def test(request):
    response = text("There's a cookie up in this response")
    response.cookies['test'] = 'It worked!'
    response.cookies['test']['domain'] = '.gotta-go-fast.com'
    response.cookies['test']['httponly'] = True
    return response

if __name__ == "__main__":
    app.run(debug = True)