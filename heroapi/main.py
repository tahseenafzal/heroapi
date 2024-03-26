from fastapi import FastAPI, HTTPException
from sqlmodel import  Session, SQLModel, create_engine, select
from .models import * 

DATABASE_URL = "postgresql://abuashja:JLR0rj8nOGCE@ep-purple-bonus-a5mp6spb.us-east-2.aws.neon.tech/todos?sslmode=require"

engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
def welcome_fast():
    return {"message":"Welcome to FastAPI SQLModel"}

@app.post("/heroes/", response_model=HeroRead)
def create_hero(hero: HeroCreate):
    with Session(engine) as session:
        db_hero = Hero.model_validate(hero)
        session.add(db_hero)
        session.commit()
        session.refresh(db_hero)
        return db_hero

@app.get("/heroes/", response_model=list[HeroRead])
def read_heroes():
    with Session(engine) as session:
        heroes = session.exec(select(Hero)).all()
        return heroes
    
@app.get("/heroes/{hero_id}", response_model=HeroRead)
def read_hero(hero_id: int):
    with Session(engine) as session:
        hero = session.get(Hero, hero_id)
        if not hero:
            raise HTTPException(status_code=404, detail="Hero not found")
        return hero