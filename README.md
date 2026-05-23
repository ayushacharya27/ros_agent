## **MAY 22 2026, 00:52 AM**
### Creating a POSTGRES SQL Setup for Storing my AgentState, if something fails

### Install Postgres
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib

sudo systemctl start postgresql

sudo systemctl status postgresql
```

### Run Postgres and Create a User
```bash
sudo -u postgres psql

CREATE DATABASE <database_name>;

CREATE USER <user_name> WITH PASSWORD '<password>';

GRANT ALL PRIVILEGES ON DATABASE <database_name> TO <user_name>;
ALTER SCHEMA public OWNER TO <user_name>;
```

### Now In Directory to Connect to it
```bash
cd <your_folder>

mkdir database && cd database

touch __init__.py # To make it as a package
touch database/__init__.py && \
touch database/database.py && \   # PostgreSQL connection
touch database/models.py && \     # SQLAlchemy models/tables
touch database/create_tables.py   # Creates DB tables
```

### Run the Database commands
```bash
python3 -m database.create_tables
```
### Creating the Agents
First I created the Planner Agent, then Wrote the Terminal tool using the tool commands

#### Calling any Code in the Directory Now, if its a package
```bash
python3 -m <package/directory_name>.<file_name>
```

Currently No Integration with the Postgre thing WhatSoever


## Ok change in Plans, now I am Planning to build a Reasoner Agent, which will call the Planner, Github etc...., and again it will call the loop










