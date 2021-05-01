Welcome to Recipe Recommender

Build the Docker Image
```sh
docker build -f Dockerfile -t streamlit-demo:latest .
```

Run the Container using
```sh
docker run -p 8501:8501 --name demo streamlit-demo
```