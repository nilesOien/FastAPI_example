#!/usr/bin/env python

# Server side python the sets up FastAPI end points
# and defines templates to be served out. The templates get
# modified by Jinja as they are served out (although
# most of this app is client side javaScript, not server
# side templates).


# Imports.
from fastapi import FastAPI, Depends, HTTPException, Query, Request
from sqlalchemy import create_engine, Column, String, Float, Integer, func
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel

from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

# Needed to handle the DotEnv file that has the database URL.
from dotenv import load_dotenv

# Needed List to return multiple results
from typing import List
import os

# Check that the pet database file exists.
if not os.path.exists("database/petdb"):
    print("The database was not found")
    print("cd into the database/ directory")
    print("and run makeDB.sh")
    quit()

# Load the enviroment file. Usually the file is named
# .env which is the default, and so it can be loaded with :
# load_dotenv()
# But because for this demo the environment file is DotEnv we use :
# load_dotenv("DotEnv")
load_dotenv("DotEnv")
dbURL = os.getenv("DATABASE_URL")
# Check that it went OK.
if dbURL is None :
    print("DATABASE_URL not in environment file DotEnv")
    quit()

# Set up tags that appear in the documentation pages that FastAPI generates.
tags_metadata = [
    {
        "name":"queryAnimals",
        "description":"Stacking of optional queries.",
        "externalDocs": {
            "description": "How this documentation was added",
            "url": "https://fastapi.tiangolo.com/tutorial/metadata/#use-your-tags",
        },
    },
    {
        "name":"listAnimalTypes",
        "description":"Nothing is passed in. The list of animal types with counts of the number in that category is returned.",
    },
    {
       "name": "favIcon",
       "description": "Small route to serve out favicon to avoid errors showing up in the server log when a browser asks for favicon if someone points their browser at the URL for a Fast API end point."
    },
    {
       "name": "root",
       "description": "Small route to serve out a friendly redirect at the root level."
    },
    {
        "name": "thePetStore",
        "description": "The main HTML template for the pet store."
    },
    {
        "name": "adjustStock",
        "description": "Adjust the number of a specific pet in stock. Used to buy or restock pets."
    }
]


# FastAPI app instance. Fill out title, etc for the docs page.
# Also set the tags that we created above.
petStore = FastAPI(title="Fast API Example",
        summary="Shows the gist of Fast API.",
        description="May be useful as an introduction to Fast API, sqlAlchemy and Jinja.",
        contact={
          "name": "Niles Oien",
          "url": "https://nso.edu",
          "email": "nilesoien@gmail.com",
        },
        version="1.0.0",
        openapi_tags=tags_metadata)


# Jinja template directory.
template = Jinja2Templates(directory="templates")

# Mounts for static studd (cascading style sheets, javaScript, and images).
petStore.mount("/static", StaticFiles(directory="static"), name="static")
petStore.mount("/js", StaticFiles(directory="js"), name="js")
petStore.mount("/images", StaticFiles(directory="images"), name="images")

# Connect to the database. There are other connection URL formats for
# other databases (postgres, mysql etc).
# We got dbURL from the environment file DotEnv, see code above
# that calls load_dotenv().
engine = create_engine(dbURL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Database model of an animal.
# A note that doesn't really apply here, but I'll mention it :
# In postgres, to connect to a table named "payroll" under a schema
# named "employee", then do NOT do this : 
#   __tablename__ = "employee.payroll";
# Instead, break out the schema like this :
#   __tablename__ = "payroll";
#   __table_args__ = {'schema': 'employee'}
#
class Animal(Base):
    __tablename__ = "pets"
    animalType = Column('animalType',  String, primary_key=True)
    animalBreed = Column('animalBreed', String, primary_key=True)
    cost = Column('cost', Float)
    desc = Column('desc', String)
    fullImage = Column('fullImage', String)
    thumbnail = Column('thumbnail', String)
    numInStock = Column('numInStock', Integer)

# Set up meta data for table.
Base.metadata.create_all(bind=engine)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Pydantic model for response data - define what an animal should look like.
# This is a pydantic class (inherits from "BaseModel" class) that is used for verification.
# When we expect one of these, or a list of these, we can say so,
# and it will be checked that we're getting at least the format we asked for.
class AnimalResponse(BaseModel):
    # This triple quoted comment winds up on the documentation page
    # for this schema.
    """
    Pydantic class that defines what comes back when an animal is requested.
    Cost is floating point in dollars and cents. Most end points return
    either one of these or a list of these.
    """
    animalType: str
    animalBreed: str
    cost: float
    desc: str
    fullImage: str
    thumbnail: str
    numInStock: int

# Pydantic class for the return of the listAnimalTypes end point (below).
# See also comments for the AnimalResponse class defined above.
class AnimalTypeResponse(BaseModel):
    # This triple quoted comment winds up on the documentation page
    # for this schema.
    """
    Pydantic class for the response to querying the animal types
    and the number of animals in each type as is done at the listAnimalTypes
    end point.
    """
    animalType: str
    num: int

# The listAnimalTypes end point.
# Takes no arguments, just returns all animal types with count.
# To get the count to have the right label for the dict for
# the AnimalTypeResponse class to handle it correctly,
# we have to apply the label "num" to the count.
# That's an important lesson for using aggregate functions.
# So you go here :
# http://127.0.0.1:8000/listAnimalTypes
# You get this :
# [
#  {
#    "animalType": "Cat",
#    "num": 5
#  },
#  {
#    "animalType": "Dog",
#    "num": 4
#  },
#  {
#    "animalType": "Fish",
#    "num": 4
#  },
#  {
#    "animalType": "Reptile",
#    "num": 3
#  }
# ]
# See populateSelector.js for how this is called from client javaScript.
@petStore.get("/listAnimalTypes", response_model=List[AnimalTypeResponse],tags=["listAnimalTypes"])
async def list_animal_types(db: Session = Depends(get_db)):
    db_animal_types = db.query(Animal.animalType, func.count(Animal.animalType).label("num")).group_by(Animal.animalType).order_by(Animal.animalType).all()
    if db_animal_types is None:
        raise HTTPException(status_code=404, detail="Problem getting animal types")
    return db_animal_types


# An "GET" endpoint that stacks queries with optional arguments
# to give the user the pets they have selected.
# With no arguments, it returns all animals, because no filters are specified.
#
# You can filter with some search criteria like so :
# http://127.0.0.1:8000/queryAnimals?minCost=50&maxCost=100&desiredType=Cat
# So, looking for cats that cost between 50 and 100
# And you get the results in this format (list of dictionaries) :
# [
#    {
#      "animalType": "Cat",
#      "animalBreed": "Maine Coon",
#      "cost": 100,
#      "desc": "Has long hair",
#      "fullImage": "MaineCoon_full.jpg",
#      "thumbnail": "MaineCoon_thumb.jpg",
#      "numInStock": 10
#    },
#    {
#      "animalType": "Dog",
#      "animalBreed": "Labradoodle",
#      "cost": 20,
#      "desc": "Low allergy dog",
#      "fullImage": "Labradoodle_full.jpg",
#      "thumbnail": "Labradoodle_thumb.jpg",
#      "numInStock": 10
#    }
# ]
#
# This is an example of how much nicer sqlAlchemy is for this stuff
# than assembling an SQL command in a string.
#
# See populateDisplayPara.js for how this is called in client side javaScript.
@petStore.get("/queryAnimals", response_model=List[AnimalResponse],tags=["queryAnimals"])
async def query_animals(db: Session = Depends(get_db), minCost: float = Query(default=None), maxCost: float = Query(default=None), desiredType: str = Query(default=None)):

    query_animals = db.query(Animal)

    # Minimum cost filter, if specified.
    if minCost is not None :
        query_animals = query_animals.filter(Animal.cost >= minCost)

    # Maximum cost filter, if specified.
    if maxCost is not None :
        query_animals = query_animals.filter(Animal.cost <= maxCost)

    # Pet type filter, if specified.
    if desiredType is not None :
        query_animals = query_animals.filter(Animal.animalType == desiredType)

    # Specify the order in which the data should be returned.
    query_animals = query_animals.order_by(Animal.animalType, Animal.cost)

    # Do the query.
    query_animals = query_animals.all()

    # Howl if something went wrong (unlikely).
    if query_animals is None:
        raise HTTPException(status_code=404, detail="Query animals returned None")

    # Return the results in JSON.
    return query_animals

# Small GET route to serve out favicon.ico for browsers.
# This is the small icon representing the page in the browser tab bar.
favicon_path = 'favicon.ico' # favicon.ico is in the root directory
@petStore.get("/favicon.ico", tags=["favIcon"])
async def serve_favicon():
    return FileResponse(favicon_path)


# Small GET route to serve out a sensible message at the root directory.
@petStore.get("/", response_class=HTMLResponse, tags=["root"])
async def serve_root(request: Request):
    return template.TemplateResponse("root.html", {"request":request})

# GET route for the actual pet store HTML template.
@petStore.get("/thePetStore", response_class=HTMLResponse, tags=["thePetStore"])
async def pet_store(request: Request):
    return template.TemplateResponse("petStore.html", {"request":request})



class messageResponse(BaseModel):
    """
    Pydantic class for the response from adjustStock POST route, which is
    a simple status message.
    """
    status: str

class adjustClass(BaseModel):
    """
    Class passed in via JSON to adjustStock POST route
    """
    animalType: str
    animalBreed: str
    adjustment: int

# POST route to adjust the number we have in stock for a pet.
# The client sends us JSON in this case and it gets turned into
# an adjustClass. See the adjustStock() function in selectPet.js
# for how this is called in javaScript.
# Return a JSON formatted status method for display in the web page.
@petStore.post("/adjustStock", response_model=messageResponse, tags=["adjustStock"])
async def adjust_stock(adjust:adjustClass, db: Session = Depends(get_db)):

    # If quantity is 0 then return. This is actually useful
    # as a pytest test.
    if adjust.adjustment == 0 :
        return { 'status': 'Quantity is zero, there is nothing to do.' }

    # Connect to the database and look up that pet.
    query_animal = db.query(Animal)
    query_animal = query_animal.filter(Animal.animalType == adjust.animalType)
    query_animal = query_animal.filter(Animal.animalBreed == adjust.animalBreed)
    query_animal = query_animal.first() # Note : first() not all() because there is only one.

    if query_animal is None:
        return { 'status': 'Operation cannot proceed, that type of pet not in database' }

    # Read the existing number in stock from the DB.
    numInDB = query_animal.numInStock
    # Get the new number in stock.
    newNumInDB = numInDB + adjust.adjustment

    # Don't let it go negative.
    if newNumInDB < 0 :
        return { 'status': 'Operation cannot proceed, only have ' + str(numInDB) + ' in stock for ' + adjust.animalBreed + ',' + adjust.animalType }

    # If it didn't go negative then it's fine, write it to the DB.
    query_animal.numInStock = newNumInDB
    db.commit()

    return { 'status': 'Success, now have ' + str(newNumInDB) + ' in stock for ' + adjust.animalBreed + ',' + adjust.animalType }



