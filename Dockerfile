#FROM python:3.11.3
#WORKDIR /app
#COPY requirements.txt .
#RUN pip install --no-cache-dir --upgrade -r requirements.txt
#COPY . .
#CMD ["/bin/bash", "docker-entrypoint.sh"]

FROM python:3.11.3
EXPOSE 5000
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["flask", "run", "--host", "0.0.0.0"]