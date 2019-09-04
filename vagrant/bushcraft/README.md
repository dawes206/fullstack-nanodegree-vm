## Item Catalog
This app is meant to be used by those who regularly backpack or bushcraft. Users can keep track of all of their gear and choose which gear to take on their next trip. Users can also see the packs of other users to get ideas about what they should add to their own supplies.


##Steps for database_setup
1. Place bushcrafwebserver.py, client_secrets.json, database_setup.py, and populateDatabase.py into the folder shared between your host machine and your VM.
2. SSH into your VM and navigate to the shared folder
3. run the command `python3 populateDatabase.py`
4. When the file finishes running, run the command `export FLASK_APP=bushcraftwebserver.py`, followed by the command `flask run --host=0.0.0.0 --port=8080`
5. Open your browser and navigate to localhost:8080 to begin using web application


## pre-requisite Knowledge
<li> Python </li>
<li> Sqlalchemy </li>

## Needed files
<li>bushcrafwebserver.py - Python script to run flask application</li>
<li>database_setup.py - Python script to define sqlalchemy framework</li>
<li>populateDatabase.py - File used to populate database</li>
<li>client_secrets.json - File used to store google sign in authorization information</li>

## API's
<li>/allPacksJson - Used to get all names, weights, and volumes of all packs in database</li>
<li>/<i>userID</i>/mypack/json - Used to get all items stored in a particular pack</li>
<li>/<i>itemID</i>/json - Used to get all details pertaining to a specific item</li>
