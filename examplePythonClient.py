#!/usr/bin/env python

# Simple pet buying client in python just to show
# that not all clients are javaScript running in web browsers.
#
# Had to 'pip install requests'
# Also had to have the FastAPI_example server going at
# http://127.0.0.1:8000 of course.

import requests

# Get the pet type from the user, have them
# select from a list.
petTypeQuery = requests.get('http://127.0.0.1:8000/listAnimalTypes')

index = 0
for item in petTypeQuery.json() :
    print(f"[ Index {index} ] : {item['animalType']} ({item['num']} available)")
    index=index+1

index=int(input("Please enter the integer index for pet type :"))
print("")

petTypes = petTypeQuery.json()
pt=petTypes[index]
petType = pt['animalType']

# OK, same for pets of that type.
petQuery = requests.get('http://127.0.0.1:8000/queryAnimals?desiredType='+petType)

index = 0
for item in petQuery.json() :
    print(f"[ Index {index} ] : {item['animalBreed']} (cost {item['cost']}) {item['desc']} {item['numInStock']} in stock")
    index=index+1

index=int(input("Please enter the integer index for the pet :"))
print("")

pets = petQuery.json()
p=pets[index]
petBreed = p['animalBreed']

quantity=int(input("Please enter the quantity to buy :"))
print("")
quantity=-quantity # Negative since we're buying not restocking

# Make a POST request with a dictionary to buy
queryBuy={}
queryBuy['animalType'] = petType
queryBuy['animalBreed'] = petBreed
queryBuy['adjustment']=quantity

buyRequest = requests.post('http://127.0.0.1:8000/adjustStock', json=queryBuy)

# Print returned status.
print(buyRequest.json()['status'])

quit()

