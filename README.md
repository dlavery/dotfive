# dotfive
Sample Application for dotfive.co.uk

## Requirement
Create an application which will allow at least two users to log in simultaneously and manage items in categories. The categories should be in a hierarchy of potentially infinite depth. The items only require a label.
The users should be able to perform standard CRUD, plus if one user makes a change, the other user(s) should see the change (if appropriate) without manually refreshing their web browser.
Your solution should follow best practice, and be robust and scalable. We expect to see the same techniques and approaches that you would use in a real project.

## Dependencies
- Python 3
- sqlite3
- Flask (pip install flask)
- SqlAlchemy (pip install sqlalchemy)

## Set Up
- Download and install Python 3 from https://www.python.org/downloads/
- Install dependent python modules flask and sqlalchemy using pip (see above)
- Unpack the repo into a local directory
- Modify scripts runtest.sh and runlive.sh to be executable ('*chmod +x <scriptname>*')
- Run tests testdb.py ('*python testdb.py*')
- Run 'test' version of the app ('*./runtest.sh*') in a separate command window
- Run tests testapi.py ('*python testapi.py*')
- Shutdown 'test' version of the app (with CTRL-C)
- Create a 'live' database ('*python schema.py dblive*')
- Run the 'live' version of the app ('*./runlive.sh*') in a separate command window
- In a browser go to the link http://localhost:5000
