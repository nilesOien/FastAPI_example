#!/bin/bash

# Run ruff checks. Relies on the ruff package being installed.
# Like uv, ruff is written in Rust and is very fast.
# It would be possible to link this to a git pre commit or
# pre push hook.
# ruff checks python indenting and general code worthiness.

# See if we are using pip in a virtual env
if [ -f "pythonEnv/bin/activate" ]
then
 source pythonEnv/bin/activate
 ruff check .
 state="$?"
 echo Exiting pip ruff check with status $state
 exit "$state"
fi

# See if we are using uv
if [ -d ".venv" ]
then
 uv run ruff check .
 state="$?"
 echo Exiting uv ruff check with status $state
 exit "$state"
fi

# Have neither uv or pip if we got here.
echo Did not find uv or pip, no ruff checks done.
exit 0


