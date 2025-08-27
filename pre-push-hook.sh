#!/bin/bash

# Pre-push git hook for FastAPI_example
# This script is run by git before a push and must exit
# with 0 status for the push to go ahead.
#
# Here, the tests that are run are the pytest tests.
#
# This cannot be checked into the right location
# as part of the repo due to
# security concerns, so to install it one must link
# it into place like so :
#
# $ ln -sf pre-push-hook.sh .git/hooks/pre-push

echo
echo Git push `date +"%Y/%m/%d %H:%M:%S %Z"` : Attempting to run git pre-push hook
echo Hook is in `pwd`/.git/hooks/pre-push
echo

# See if we have the database - if not, not much testing can happen.
if [ ! -f "database/petdb" ]
then
 echo Database not found, no pre-push tests can be done, accepting push
 exit 0
fi

# See if we are using pip in a virtual env
if [ -f "pythonEnv/bin/activate" ]
then
 source pythonEnv/bin/activate
 pytest -v
 state="$?"
 echo Exiting pip test with status $state
 exit "$state"
fi

# See if we are using uv
if [ -d ".venv" ]
then
 uv run pytest -v
 state="$?"
 echo Exiting uv test with status $state
 exit "$state"
fi

# Have neither uv or pip if we got here.
echo Pre-push test did not find either uv or pip, no test done
exit 0


