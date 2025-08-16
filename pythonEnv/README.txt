
First, build a python virtual environment, using a recent
version of python (roughly, 3.9 or greater).

I did this in $HOME/FastAPI_example/pythonEnv/
You will have to substitute your own path in the
commands below.

To build the virtual environment :
 $ python -m venv $HOME/FastAPI_example/pythonEnv

NOTE : On a Mac, you may have to use "python3" rather than
"python" for the above step. 

To activate the virtual environment :
 $ source $HOME/FastAPI_example/pythonEnv/bin/activate

The command prompt should change to reflect the fact
that the virtual environment is now being used. You can check
by checking which python binary the system has in its path,
so the command prompt should look like this :

(pythonEnv) $

You definitely want that so that ensuing changes/installs
only affect the virtual environment.

Update the pip installer (just so it doesn't complain
about using an out of date pip) :
(pythonEnv) $ pip install --upgrade pip

Then install the python modules :

(pythonEnv) $ pip install sqlalchemy sqlalchemy-utils
(pythonEnv) $ pip install fastapi pydantic uvicorn
(pythonEnv) $ pip install email-validator jinja2

The python environment is now set up. The database can now
be built as described in the main instructions.

