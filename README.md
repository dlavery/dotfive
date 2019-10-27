# dotfive
Sample Application for dotfive.co.uk

## Requirement
Create an application which will allow at least two users to log in simultaneously and manage items in categories. The categories should be in a hierarchy of potentially infinite depth. The items only require a label.
The users should be able to perform standard CRUD, plus if one user makes a change, the other user(s) should see the change (if appropriate) without manually refreshing their web browser.
Your solution should follow best practice, and be robust and scalable. We expect to see the same techniques and approaches that you would use in a real project.

## Dependencies
- Python 3
- SQLite
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

## Notes
- This represents about 5-6 hours work over 3 days.
- The application is basic; enhancements would include a better UI, including ways to distinguish categories from items (other than by context), and verious technical improvements.
- User authorisation is not implemented; normally authentication/authorisation would be implemented not with a custom-built component but by integration with Facebook or Google identities, or a service such as Okta (https://www.okta.com/).
- SQLite is not a database engine for production use; the SQLAlchemy ORM has been used to abstract the application from the database implementation so that a production quality DB could be easily substituted.
- For expediency reasons, APIs have been created that are bound to the front end app rather than written for general use; this should be refactored prior to production use of this application.
- Change notification between users not implemented; this would be implemented with a pub/sub framework, a messaging service such as AWS SQS, or a database that supports pub/sub (such as Redis).
- Flask would normally be productionised with Gunicorn or by hosting the app on AWS or the Google App Engine.
