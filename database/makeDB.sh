#!/bin/bash

# Clean up any existing database file and then
# run the python that makes the database. Requires
# being in the virtual environment, so source the 
# activation script for that.

/bin/rm -f petdb
source ../pythonEnv/bin/activate
./makeDB.py

exit 0

