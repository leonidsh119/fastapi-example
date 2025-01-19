# Microservice Example 

### The example microservice exposes the following endpoints:
- REST API endpoints
  - SwaggerUI on /docs
  - Healthcheck on /health
  - Publish message to RabbitMQ on /notification
  - Example CRUD on /items
- RabbitMQ
  - Subscriber
  - Publisher

### The example based on the tech. stack below:
- Python 3.13
- FastAPI
- uvicorn server
- Settings management using .env file
- .venv
- poetry package manager
- Dockerfile

## Build:
````
docker build -t fastapi-example .
````

## Run
- run independently
````
docker run -d -p 8000:8000 --network host --name example_container fastapi-example
docker run -d --name rabbit-mq -p 5672:5672 -p 15672:15672 rabbitmq:management
````

- run in compose with RabbitMQ container
````
docker-compose up
````

## Test
when the containers are up and running together:
- Test the application REST API on  http://127.0.0.1:8000/docs
- Publish messages on RabbitMQ: http://localhost:15672/ (login with default credentials: guest/guest)
- The automated testing is implemented using PyTest. The tests are testing REST endpoints and mocking the connection to RabbitMQ. Run the tests by:
````
poetry run pytest
````