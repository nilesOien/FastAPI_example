#!/bin/bash

# This starts the server. The syntax is :
# uvicorn path:appName
#
# So that
# uvicorn FastAPI_example:petStore
# means look in FastAPI_example.py and start the application petStore in there
#
# Dots are used to delimit directories in that, so if the path were
# ./some/dir/path/FastAPI_example.py
# then the command would be
# uvicorn some.dir.path.FastAPI_example:petStore

if [ ! -f "database/petdb" ]
then
    echo "The database was not found"
    echo "cd into the database/ directory"
    echo "and run makeDB.sh"
    exit -1
fi

source pythonEnv/bin/activate

uvicorn FastAPI_example:petStore --host 127.0.0.1 --port 8000 --workers 1

exit 0

