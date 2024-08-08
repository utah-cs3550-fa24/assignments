Installing all of the Software
==============================

Installing Python
-----------------

Find or install Python 3, at least version 3.10 but newer is better.
Check your Python version with:

    python3 --version

On some machines, you might need to use `python` instead of `python3`.
But make sure it is prints Python 3 3.10 or above, not the obsolete
Python 2 or an older Python 3.

CADE machines have Python 3.10 installed. On macOS, Python comes
preinstalled, but it may be out of date. Python is available for all
platforms from [python.org]. (You can also install Python through VS
Code, Homebrew, your system package manager, or any other source, as
long as it is recent enough.)

Make sure that your Python has database support:

    python3 -c "import sqlite3"

If this command succeeds with no output, that means you have database
support. This should be the case for most Python installations. If you
see what looks like an error, seek help from the instructors.

Installing Django
-----------------

Install Django by running:

    python3 -m pip install django

Check your Django version by running:

    python3 -m django --version
    
Make sure the version starts with 5.0.
