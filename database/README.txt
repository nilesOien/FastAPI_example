
After setting up the python virtual environment in the
directory ../pythonEnv, run the script makeDB.sh to build the
database by reading the JSON in pets.json and writing an
sqlite database file named "petdb". Run it like this :

$ ./makeDB.sh

If you have sqlite3 installed, you can then look at the
database (optional) like so :

# Enter sqlite3 to look at petdb
$ sqlite3 petdb 
SQLite version 3.34.1 2021-01-20 14:10:07
Enter ".help" for usage hints.

# List the available tables - should only be "pets"
sqlite> .tables
pets

# Describe that table.
sqlite> .schema pets
CREATE TABLE pets (
	"animalType" VARCHAR NOT NULL, 
	"animalBreed" VARCHAR NOT NULL, 
	cost FLOAT, 
	"desc" VARCHAR, 
	"fullImage" VARCHAR, 
	thumbnail VARCHAR, 
	PRIMARY KEY ("animalType", "animalBreed")
);

# See what is in the table.
sqlite> select * from pets;
Dog|Doberman|50.0|Good guard dog|Doberman_full.jpg|Doberman_thumb.jpg
Dog|Labradoodle|20.0|Low allergy dog|Labradoodle_full.jpg|Labradoodle_thumb.jpg
Dog|German Shepherd|70.0|Needs a lot of space|GermanShepherd_full.jpg|GermanShepherd_thumb.jpg
Dog|Daschund|120.0|Get a long, little doggie|Daschund_full.jpg|Daschund_thumb.jpg
Cat|Siamese|30.0|Actual cat may not be from Siam|Siamese_full.jpg|Siamese_thumb.jpg
Cat|Tabby|10.0|The classic cat|Tabby_full.jpg|Tabby_thumb.jpg
Cat|Maine Coon|100.0|Has long hair|MaineCoon_full.jpg|MaineCoon_thumb.jpg
Cat|Persian|80.0|A good hunter if you have mice|Persian_full.jpg|Persian_thumb.jpg
Cat|Burmese|45.0|Very active cat|Burmese_full.jpg|Burmese_thumb.jpg
Fish|Guppy|0.5|The minimal fish|Guppy_full.jpg|Guppy_thumb.jpg
Fish|Goldfish|2.5|The classic fish|Goldfish_full.jpg|Goldfish_thumb.jpg
Fish|Shark|500.0|High end exotic fish|Shark_full.jpg|Shark_thumb.jpg
Fish|Pirana|250.0|Only order this if you know what you're doing|Pirana_full.jpg|Pirana_thumb.jpg
Reptile|Bearded dragon|25.0|Classic lizard pet|BeardedDragon_full.jpg|BeardedDragon_thumb.jpg
Reptile|Boa constrictor|250.0|Can grow to be very large|BoaConstrictor_full.jpg|BoaConstrictor_thumb.jpg
Reptile|Gecko|15.0|Often found in the wild|Gecko_full.jpg|Gecko_thumb.jpg

# Exit sqlite with CNTRL-D
sqlite> ^D

