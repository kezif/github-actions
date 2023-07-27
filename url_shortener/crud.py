from sqlalchemy.orm import Session
# from Crypto.Hash import SHA256
from . import models, schemas


def compact_slot(slot) -> str:
    # get first 5 numbers not counting indexet at 0
    return str(slot)[1:6]

def validator(db: Session, og_url: schemas.UrlCreate, slot: str, c_slot=compact_slot) -> bool:
    # return True if slot is empty 
    # and item if slot doesn't equal the key
    if get_url_byshorten(db, c_slot(slot)):  # check if slot is occupied
        return False
    if url := get_url_byoriginal(db, og_url):  # always false if used only inside create_shorten_link
        if url.shorten_url != c_slot(slot):
            return False
    return True


def generate_short_link(db: Session, og_url: schemas.UrlCreate, val=validator, c_slot=compact_slot) -> str:
    # transforms www.site.domain to XXXXX
    # open addressing for of avoiding collision / algorithm stealed from python source code
    h = hash(og_url.original_url)
    slot = h
    perturb = h
    
    while (not val(db, og_url, slot)):
        slot = (5*slot) + 1 + perturb
        perturb >>= 5
         
    return c_slot(slot)

def create_shorten_link(db: Session, og_url: schemas.UrlCreate):
    shorten_url = generate_short_link(db, og_url)

    db_url = models.Url(original_url=str(og_url.original_url), shorten_url=shorten_url)
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url

def inc_number_of_cliks(db: Session, shorten_url: str):
    db.query(models.Url).filter(models.Url.shorten_url == shorten_url).\
        update({'clicks': models.Url.clicks + 1})  # update number of cliks
    db.commit()

'''def inc_number_of_cliks2(db: Session, url: models.Url):
    url.clicks += 1
    db.commit()'''
    
'''def get_original_link(db: Session, shorten_url: str):
    check_exists = get_url_byshorten(db, shorten_url)
    if not check_exists:
        return None
    
    return check_exists.original_url'''

def get_url_byshorten(db: Session, shorten_url: str):
    return db.query(models.Url).filter(models.Url.shorten_url == shorten_url).first()


def get_url_byoriginal(db: Session, original_url: schemas.UrlCreate):
    return db.query(models.Url).filter(models.Url.original_url == str(original_url.original_url)).first()


def get_links(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Url).offset(skip).limit(limit if limit<=100 else 100).all()
