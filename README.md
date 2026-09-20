# findmushroom

### About app
This is data science project for helsinki universitys masters course. 

### Installation
1. pull the repo ```git pull git@github.com:FungusLocus/findmushroom.git ```
2. go to the project root ```cd findmushroom```
3. create virtual enviroment ```python -m venv .venv``` (linux)
4. activate venv ```source .venv/bin/activate```
5. install requirements ```pip install -r requirements.txt```

### Running the app
1. ``` source .venv/bin/activate ``` 
2. ```uvicorn app.main:app --reload```


### Datasets used
[Mushroom data](https://laji.fi/en)

[Weather data](https://www.ilmatieteenlaitos.fi/suomen-havainnot/asema?station=108040)

### Database set up

1. Install [PostgreSQL](https://www.postgresql.org/download/)
2. Open pgAdmin
3. Connect to PostgreSQL with the username and password you made during installation
4. Create a new database
5. Open the query tool and execute the content of database/schema.sql

### Architecture
- nice little mermaid pic

### Machine learning choices
- what we using and why

### Some math about how good our model is :D
- accuracy and overfitting scores?
