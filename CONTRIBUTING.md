# contributing

## how to run docker locally

```
firts build the docker image
docker build -t ...... image_name .
docker run -dp 5000:5000 -w /app -v "$(pwd):/app" <image_name> sh -c "flask run --host 0.0.0.0"
```

```dockerfile dev
FROM python:3.11.3
EXPOSE 5000
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["flask", "run", "--host", "0.0.0.0"]
```