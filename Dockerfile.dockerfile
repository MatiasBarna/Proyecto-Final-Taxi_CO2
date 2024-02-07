FROM python:3.8

WORKDIR /app

COPY requirements.txt ./requirements.txt

RUN pip3 install -r requirements.txt

EXPOSE 8080

COPY . /app


CMD ["streamlit", "run", "app.py"]
