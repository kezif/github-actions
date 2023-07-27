from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse

from . import crud, models, schemas
from .database import SessionLocal, engine


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/')
def main_entry():
    '''Welcome to the link shortener service. Access /docs to see how to use api'''
    return {'Welcome': 'Welcome to the link shortener service. Access /docs to see how to use api!'}


@app.post('/', response_model=schemas.Url_)
def create_short_url(og_url: schemas.UrlCreate, db: Session = Depends(get_db)):
    check_exists = crud.get_url_byoriginal(db, og_url)
    if check_exists:
        return check_exists
    return crud.create_shorten_link(db, og_url)


@app.get('/{shorten_url}', response_model=schemas.UrlBase)
def redirect_to_original(shorten_url: str, db: Session = Depends(get_db)):
    url = crud.get_url_byshorten(db, shorten_url)
    if not url:
        raise HTTPException(status_code=400, detail="Url does not exists")
    
    # crud.inc_number_of_cliks(db, shorten_url)
    # crud.inc_number_of_cliks2(db, url)
    return url
    # return RedirectResponse(url.original_url)


@app.get('/info/{shorten_url}', response_model=schemas.Url_)
def get_linkinfo(shorten_url: str, db: Session = Depends(get_db)):
    url = crud.get_url_byshorten(db, shorten_url)
    if not url:
        raise HTTPException(status_code=400, detail="Url does not exists")
    
    return url

@app.get('/debug/links', response_model=list[schemas.Url_])
def get_all_links_DEBUG(skip: int = 0, limit: int = 100,db: Session = Depends(get_db)):
    items = crud.get_links(db, skip=skip, limit=limit)
    return items

 


'''@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)'''