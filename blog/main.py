from urllib import response

from fastapi import FastAPI, Depends, Response
from . import schemes, models
from .database import engine, SessionLocal
from sqlalchemy.orm import Session
from . import models, database
from passlib.context import CryptContext

app = FastAPI()
models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/blog', status_code=201, tags=['blogs'])
def create_blog(request: schemes.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.get('/blog', status_code=200, tags=['blogs'])
def get_blogs(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@app.get('/blog/{id}', status_code=200, tags=['blogs'])
def show(id: int, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        response.status_code = 404
    return blog


@app.delete('/blog/{id}', status_code=204, tags=['blogs'])
def delete_blog(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        response.status_code = 404
    blog.delete(synchronize_session=False)
    db.commit()


@app.put('/blog/{id}', status_code=202, tags=['blogs'])
def put_blog(id: int, request: schemes.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).update(request)
    if not blog.first():
        response.status_code = 404
    blog.update(request)
    db.commit()


pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")


@app.post('/user', response_model=schemes.ShowUser, tags=['User'])
def create_user(request: schemes.User, db: Session = Depends(get_db)):
    hashed_password = pwd_cxt.hash(request.password)
    new_user = models.User(name=request.name, email=request.email, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user



@app.get('/user{id}', response_model=schemes.ShowUser, tags=['User'])
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        response.status_code = 404
