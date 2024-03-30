from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_post():
    return {'data': "World"}


@app.get("/post/{id}")
def dt_post(id: int):
    return {'data': id}


@app.get('/post/{id}/comment')
def comment(id: int):
    return {'data':
                {'comment': 1}
            }
