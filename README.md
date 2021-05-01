Welcome to Recipe Recommender



Run the Application with the Docker container running in the background with docker-compose.
```sh
docker-compose up -d
```

Tear down the application, either by stopping the application using
```sh
docker-compose down
```
or to stop the application, remove the stopped containers and optionally --rmi all / remove all images associated in the docker-compose.yml file
```sh
docker-compose down --rmi all
```