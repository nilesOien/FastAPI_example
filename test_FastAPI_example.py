#!/usr/bin/env python

# A series of tests to run with pytest.
# Tests the JSON delivered by FastAPI endpoints.
#
# pytest is run by the runTests.sh script.
#
# pytest looks for any file named test_* and runs
# functions named test_* in those files.

from fastapi.testclient import TestClient
from fastapi import status
from .FastAPI_example import petStore

client=TestClient(petStore)

# Test the listAnimalTypes end point (get method).
# Returned JSON should be something like :
# [{"animalType":"Cat","num":5},{"animalType":"Dog","num":4},{"animalType":"Fish","num":4}]
# Check the status returned and the keywords in the JSON list.
def test_listAnimalTypes():
    response=client.get("/listAnimalTypes")
    assert response.status_code == status.HTTP_200_OK
    for item in response.json() :
        assert 'animalType' in item
        assert 'num' in item

# Similar for queryAnimals end point (also get method).
# Now, we could ask for one specific animal and test
# that we get exactly that from the database, but that
# would rely on the dat.abase not changing for the test
# to always work. So don't do that. Instead just test
# keywords like we did above. Also check cost > 0.
# JSON should be something like :
#  {
#    "animalType": "Dog",
#    "animalBreed": "Labradoodle",
#    "cost": 20,
#    "desc": "Low allergy dog",
#    "fullImage": "Labradoodle_full.jpg",
#    "thumbnail": "Labradoodle_thumb.jpg",
#    "numInStock": 10
#  },
#  {
#    "animalType": "Dog",
#    "animalBreed": "Doberman",
#    "cost": 50,
#    "desc": "Good guard dog",
#    "fullImage": "Doberman_full.jpg",
#    "thumbnail": "Doberman_thumb.jpg",
#    "numInStock": 10
#  }
def test_queryAnimals():
    response=client.get("/queryAnimals?minCost=10&maxCost=50&desiredType=Dog")
    assert response.status_code == status.HTTP_200_OK
    for item in response.json() :
        assert 'animalType' in item
        assert 'animalBreed' in item
        assert 'cost' in item
        assert 'desc' in item
        assert 'fullImage' in item
        assert 'thumbnail' in item
        assert 'numInStock' in item
        assert item.get('cost') > 0.0




# Test the post method. Send it a quantity of zero so that the database is
# not affected by testing. Constant JSON should be returned.
def test_adjustStock():
    response=client.post("/adjustStock", json={"adjustment":0, "animalBreed":"Burmese", "animalType":"Cat"})
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == { 'status': 'Quantity is zero, there is nothing to do.' }

# Test on a stock adjustment to a non-existant pet.
def test_noSuchPet():
    response=client.post("/adjustStock", json={"adjustment":1, "animalBreed":"Horned", "animalType":"Elephant"})
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == { 'status': 'Operation cannot proceed, that type of pet not in database' }
