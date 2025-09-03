#!/usr/bin/env python

# Small script that reads the file pets.json and creates
# an sqlite database with a table named pets that has
# the list of pets available in a pet store in it.
#
# Deletes the table before writing to it so that it can
# be run repeatedly.
#
# Demonstration of a simple use of relating to a database 
# with sqlalchemy.

from sqlalchemy import create_engine, UniqueConstraint, Column, String, Float, Integer
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import declarative_base, sessionmaker
import json
import os

# Make a table, the column names of which line
# up with what we have in the JSON. Table name is "pets".
# Unique constraint ensures only one entry for (animalType, animalBreed).
# Arbitrarily added some primary keys. None of this data is nullable.
Base = declarative_base()

class petTable(Base):
    __tablename__='pets'
    animalType  = Column(String,  nullable=False, primary_key=True)
    animalBreed = Column(String,  nullable=False, primary_key=True)
    cost        = Column(Float,   nullable=False, primary_key=True)
    desc        = Column(String,  nullable=False)
    fullImage   = Column(String,  nullable=False)
    thumbnail   = Column(String,  nullable=False)
    numInStock  = Column(Integer, nullable=False)
    __table_args__ = (UniqueConstraint('animalType', 'animalBreed', name='unique_constraint'),)

# Create the database.
# Had to install sqlalchemy_utils to do this.
engine = create_engine("sqlite:///petdb", echo=False)

Base.metadata.create_all(engine)

if not database_exists(engine.url):
    create_database(engine.url)

# Drop any existing version of that table.
# It was important to make the table first, othwerwise
# drop_all doesn't know what table we're talking about.
Base.metadata.drop_all(engine)

# OK, now create the empty table. Turn echo on, just for this.
engine.echo=True
Base.metadata.create_all(engine)
engine.echo=False

# Read in the JSON text file which looks something like this :
# { "petList" : [
#  { "animalType":"Dog",    "animalBreed":"Daschund",        "cost":120.00,
#    "desc":"Get a long, little doggie",
#    "fullImage":"Daschund_full.jpg", "thumbnail":"Daschund_thumb.jpg",
#    "numInStock": 10 },
#  { "animalType":"Cat",    "animalBreed":"Siamese",         "cost":30.00,
#    "desc":"Actual cat may not be from Siam",
#    "fullImage":"Siamese_full.jpg", "thumbnail":"Siamese_thumb.jpg",
#    "numInStock": 10 }
# ] }
# Many lines omitted but you get the idea - it's a list of dicts.

if not os.path.exists("pets.json") :
    print("The file pets.json not found, database will be empty")
    quit()

# Read all lines from the file (it's fairly small)
f = open("pets.json", "r")
petLines = f.readlines()
f.close()

# Append all lines to one string, using rstrip() to remove control codes.
petsString = ""
for line in petLines :
    petsString = petsString + line.rstrip()

# Turn that JSON formatted string into an object.
# Say something and exit if the formatting is wrong.
try :
    x = json.loads(petsString)
except Exception as e :
    print(f"File pets.json formatting problem : {type(e)} : {e}")
    quit()

print(f"Found {len(x['petList'])} pets in file pets.json")

# Create a session to do data insert from dictionary list.
Session = sessionmaker(bind=engine)
session = Session()

ok=False
try:
    # Use bulk_insert_mappings (more efficient for large datasets)
    session.bulk_insert_mappings(petTable, x['petList'])
    session.commit()
    print("Data inserted successfully.")
    ok=True

except Exception as e:
    session.rollback() # Rollback on error
    print(f"Error inserting data : {e}")
    ok=False

finally:
    session.close()

# That's all - the database should be created.
if ok :
    print("Normal termination.")
else :
    print("Something went wrong")

quit()

