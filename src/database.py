import os

from dotenv import load_dotenv

from sqlalchemy import create_engine, desc 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from src.models.links import Link as ModelLink
from src.models.real_estates import RealEstates as ModelRealEstates

load_dotenv('.env')

SQLALCHEMY_DATABASE_URL = os.environ["DATABASE_URI"]
engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def add_offers(list_of_offers) -> None:
    offers_to_save = []
    with SessionLocal() as db:
        for offer in list_of_offers:
            offers_to_save.append(ModelRealEstates(url = offer["url"],
                                    description = offer["description"],
                                    total_price = offer["total_price"],
                                    price = offer["price"],
                                    rent = offer["rent"],
                                    currency = offer["currency"],
                                    area = offer["area"],
                                    rooms = offer["rooms"],
                                    deposit = offer["deposit"],
                                    floor = offer["floor"],
                                    type = offer["type"],
                                    status = offer["status"],
                                    region = offer["region"],
                                    )
                                )
        db.add_all(offers_to_save)
        db.commit()


def set_link_as_used(url):
    with SessionLocal() as db:
        row = db.query(ModelLink).filter_by(url=url).one()
        row.used = True
        db.commit()
    

def select_unused_and_active_links(city: str):
    with SessionLocal() as db:
        links_details = db.query(ModelLink).filter_by(city_name=city,
                                                      used=False,
                                                      is_active=True).all()
        return links_details
