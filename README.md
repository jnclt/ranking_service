# Ranking Service

Service allows to create/update a player's score in a given category (metric).
Service allows to retrieve a list of top x/all scores for a given category and/or player.

# Docs

Relative URL of the serivce is '/rankings/'.
For API description, please see the docstrings in rankings/views.py

# Discussion

- How would you test this?
> Tests are in ./tests folder. See below how to run them.

- What would you do if you were told this needs to handle 1 million players?
> 1. Integrate a proven REST framework (i.e. Django REST / Tastypie) to get caching, authentication, pagination, ...
> 2. Run the service on a number of Apache instances behind a load balancer
> 3. Use a (possibly NoSQL) distributed database that allows masterless replication (Cassandra).
> 4. Monitor the load  
> 5. Alternatively, I'd consider Erlang-based stack with CouchDB and Yaws :)

# Installation

## 1. Create and/or activate a Virtual Environment

```bash
. activate_venv
```

## 2. Install dependencies
```bash
./install_dependencies
```

## 3. Synchronize Database

```bash
./manage.py syncdb --noinput
```

## 4. Run the application

```bash
./run_server
```

# Tests

## Analyze Source code
```bash
./analyze
```

## Run Tests

```bash
./run_tests [ unit | integration | system ]
```
