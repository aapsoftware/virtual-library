# Virtual Library App

# Building and running the app in a docker container

```
docker-compose up
```

# Stopping the containser

```
docker-compose stop
```

# Removing the containser and starting over

```
docker-compose up
```

# Runing unit tests
```
docker build -f Dockerfile.build -t virtual-library-builder .
docker build -f Dockerfile.tests .
```

# About the app
 An initial db is added to the image which contains a few book titles

# The API
To see the API documentation:
- in your browser, after bring up the container, go to http://localhost:7777/api/v1/
- check out the swagger.yaml included in the project

  There are two enpoints
    - one to manage book titles:

```
    get all book titles:
    curl -i -X GET "http://localhost:7777/api/v1/book"

    add a book title
    curl -i -X POST "http://localhost:7777/api/v1/book/<new_book_title>"

    get a book title
    curl -i -X GET "http://localhost:7777/api/v1/book/<desired_book_title>"
```

    - one to manage book titles:

```
    get all book requests:
    curl -i -X GET "http://localhost:7777/api/v1/request"

    add a book request
    curl -i -X POST "http://localhost:7777/api/v1/request?email=<email>&title=<title>"

    get a book requests
    curl -i -X GET "http://localhost:7777/api/v1/book/<book_request_id>"
```