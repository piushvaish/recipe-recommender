Welcome to Recipe Recommender

Project structure is as follows:

.
├── data
├── docker-compose.yml
├── Dockerfile
├── images
│   ├── heart-logo.png
│   └── bookmark.png
|   └── etc.
|── model
├── LICENSE
├── project
│   └── app.py
├── README.md
└── requirements.txt


Build the Docker Image
```sh
docker build -f Dockerfile -t streamlit-demo:latest .
```

Run the Container using
```sh
docker run -p 8501:8501 --name demo streamlit-demo
```