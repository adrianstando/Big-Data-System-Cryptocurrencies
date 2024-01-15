FROM python:3.11-bookworm

RUN apt-get -y update

COPY . /app
WORKDIR /app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "80"]
EXPOSE 80
