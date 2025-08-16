# FastAPI_example

This is an example of how some technologies can work together, namely :

1. Python FastAPI running on a server, providing endpoints
   that send JSON formatted information (see FastAPI_example.py)
2. The uvicorn server sending to the client (see the startServer.sh script)
3. Jinja doing template substitutions as HTML is served out by uvicorn
   (see the template HTML files in the templates directory)
4. javaScript running on the client, interacting with the user and
   getting data from FastAPI endpoints as required (see the js directory)
5. Cascading style sheets (CSS) controlling some aspects of the HTML appearance
   (see the static directory)
6. The sqlAlchemy python object relational manager (ORM)

You should be able to set this up fairly quickly,
then see it run in a browser. Put the browser in debug
mode to see the data moving between client and server.

## Section 1.0 Set up - Python virtual environment

**NOTE** : You may want to consider following the steps in section 6.0
and 7.0 to use the **uv** package manager rather than following
the steps in this section, which use the **pip** package manager with a
virtual environment
rather than uv. If you're considering that, then read sections 1.0, 6.0
and 7.0 first.

To use a pip/virtual environment,
first set up the python virtual environment in the pythonEnv directory
and install the required python modules with the following
terminal commands (assuming the directory you have is $HOME/FastAPI_example) :

```
$ python -m venv $HOME/FastAPI_example/pythonEnv
```
**NOTE** : On a Mac, you may have to use "python3" rather than
"python" for the above step. 

To activate the virtual environment :
```
 $ source $HOME/FastAPI_example/pythonEnv/bin/activate
```
The command prompt should change to reflect the fact
that the virtual environment is now being used. You can check
by checking which python binary the system has in its path,
so the command prompt should look like this :
```
(pythonEnv) $
```
**You definitely want to be in the virtual enviroment
with the changed prompt, so that ensuing changes/installs
only affect the virtual environment and not the system python.**

Update the pip installer (just so that it doesn't complain
about using an out of date pip when it does installs) :
```
(pythonEnv) $ pip install --upgrade pip

```
Then install the python modules :
```
(pythonEnv) $ pip install sqlalchemy sqlalchemy-utils
(pythonEnv) $ pip install fastapi pydantic uvicorn
(pythonEnv) $ pip install email-validator jinja2
```

You can now leave the python virtual environment, it
will be invoked as needed by the scripts. To leave :

```
(pythonEnv) $ deactivate
```

## Section 2.0 Set up - Building the database

To build the simple sqlite database that the system needs,
use the following terminal commands
(again assuming the directory you have is $HOME/FastAPI_example) :

```
$ cd $HOME/FastAPI_example/database
$ ./makeDB.sh
```

You should see a message that the script had normal termination,
and you should have a file named petdb.

## Section 3.0 Running the server

The terminal commands to run the example are :

```
$ cd $HOME/FastAPI_example
$ ./startServer.sh
```

It should say something like :

```
INFO:     Started server process [102618]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

## Section 4.0 Running the server

Point a browser at
[http://127.0.0.1:8000](http://127.0.0.1:8000 "The main page")

Put the browser in debug mode to see the JSON formatted data going
between the server and the client to respond to user requests.


## Section 5.0 Extra : Adding tests

To add tests, we need to install a couple more python packages
in the virtual enviroment. To do that, get into the
virtual environment and install them like so :
```
$ source $HOME/FastAPI_example/pythonEnv/bin/activate
(pythonEnv) $ pip install httpx pytest
(pythonEnv) $ deactivate
$
```

You can now run the tests in the file test_FastAPI_example.py
by running the runTests.sh script :
```
$ ./runTests.sh
============================= test session starts ==============================
platform darwin -- Python 3.9.6, pytest-8.4.1, pluggy-1.6.0
rootdir: /Users/noien/FastAPI_example
plugins: anyio-4.10.0
collected 3 items                                                                                                      

test_FastAPI_example.py ...                                       [100%]

============================== 3 passed in 1.39s ===============================
```
The tests themselves are documented in test_FastAPI_example.py


## Section 6.0 Using uv instead of pip and virtualenv

Much of this discussion was taken from
[https://docs.astral.sh/uv/guides/migration/pip-to-project/](https://docs.astral.sh/uv/guides/migration/pip-to-project/ "The uv migration page")

**uv** is a package manager for python. It is very fast. It
is written in Rust. It replaces pip and a virtual environment,
which is what was used in section 1.0 here to install this
system.

A key difference between uv and the pip/virtual environment approach
is that pip/virtual environment relies on an environment being
active, whereas uv uses "uv run" to execute python in a
virtual environment that it manages.

So while to run the tests in pip/virtual environment we might
activate the virtual environment, run pytest, and then
exit the environment, like this :
```
$ source $HOME/FastAPI_example/pythonEnv/bin/activate
(pythonEnv) $ pytest
(pythonEnv) $ deactivate
$
```
in uv we would do this :
```
$ uv run pytest
```

In this example the pip virtual environment is in the
pythonEnv/ directory, but uv puts the environment in a hidden
directory named .venv/

To use uv instead of pip/virtual environment, first 
install uv. This is best done like so :
```
$ curl -LsSf https://astral.sh/uv/install.sh | sh
```

This will install uv for you only (not system wide).

Then in the FastAPI_example/ directory we can
initialize uv in the current directory, giving it a 
name and a description, and telling
it not to generate a README.md file since in this case
we already have one : 
```
$ uv init --name FastAPI_example --description "An example of FastAPI" --no-readme .
```
This will write a file named pyproject.toml :
```
$ cat pyproject.toml 
[project]
name = "fastapi-example"
version = "0.1.0"
description = "An example of FastAPI"
requires-python = ">=3.13"
dependencies = []
```
but note that the file lists no dependencies yet.

We then create a file, requirements.in (included here) that lists the modules
that we use. These modules would have been installed with pip when we were using
pip with a virtual environment. The file looks like this (the test
modules httpx and pytest are included) :
```
$ cat requirements.in 
sqlalchemy
sqlalchemy-utils
fastapi
pydantic
uvicorn
email-validator
jinja2
httpx
pytest
```
This file has been created and is included here.

As an aside, it's also possible to take an existing pip 
install and do this in the virtual environment :
```
(pythonEnv) $ pip freeze > requirements.txt
```
which would write the file requirements.txt that lists the modules
**and** includes the version of each module (as opposed to
requirements.in which just lists the modules).
This can be used
if you have a pip install and want to migrate to
uv, but want to preserve existing module versions.

In our case, we can add the dependencies to  :
our pyproject.toml file with :
```
$ uv add -r requirements.in
```

Which results in the dependencies, with the versions that uv finds,
being added to the pyproject.toml file :
```
$ cat pyproject.toml 
[project]
name = "fastapi-example"
version = "0.1.0"
description = "An example of FastAPI"
requires-python = ">=3.13"
dependencies = [
    "email-validator>=2.2.0",
    "fastapi>=0.116.1",
    "httpx>=0.28.1",
    "jinja2>=3.1.6",
    "pydantic>=2.11.7",
    "pytest>=8.4.1",
    "sqlalchemy>=2.0.43",
    "sqlalchemy-utils>=0.41.2",
    "uvicorn>=0.35.0",
]
```

If we wanted to preserve existing pip versions with a requirements.txt
from **pip freeze**
then we could have used requirements.txt as a constraint by
working backwards to generate requirements.in from requirements.txt
by leaving out the version information using awk :
```
$ cat requirements.txt | awk -F= '{print $1}' > requirements.in
```
And then running uv add with that constraint :
```
$ uv add -r requirements.in -c requirements.txt
```
But we are not doing that here.

In any event, we can now set up the database 
as discussed in section 2.0 with the
uv version of makeBD.sh which is named uv_makeBD.sh :
```
$ cd database
$ ./uv_makeBD.sh
$ cd ..
```
The uv_makeBD.sh script just does this :
```
$ uv run makeDB.py
```

Similarly we can then run pytest tests,
as discussed in section 4.0, with the uv version of
runTests.sh, named uv_runTests.sh :
```
$ ./uv_runTests.sh
```
which just does :
```
$ uv run pytest
```

And similarly the server can be started, 
as discussed in section 3.0, with the uv version of the start script :
```
$ ./uv_startServer.sh 
INFO:     Started server process [39602]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

If uv is used, then the pythonEnv/ directory becomes redundant, and the steps
in section 1.0 should **not** be taken.

## 7.0 Quickstart with uv

This is how to get things going quickly under the uv package builder.
This section is basically a rapid-fire version of section 6.0.

First, if you don't have uv installed, install it and
source the file that is needed after install for uv to be in your path :
```
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env
```

Then do the following to :
1. Initalize the uv project
2. Add the requirements (and marvel at how fast
the Rust based uv system sets up the environment with those requirements)
3. Build the database
4. Run the unit tests in pytest
5. Start the server
```
cd FastAPI_example/
uv init --name FastAPI_example --description "An example of FastAPI" --no-readme .
uv add -r requirements.in
cd database/
./uv_makeBD.sh 
cd ../
./uv_runTests.sh 
./uv_startServer.sh 
```

You should see something like this :
```
$ ./uv_startServer.sh 
INFO:     Started server process [2805]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)

```
At which point you can point a browser at 
[http://127.0.0.1:8000](http://127.0.0.1:8000 "The main page")
and turn on debugging in the browser and watch the JSON messages
fly back and forth between the client and the server.
