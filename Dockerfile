FROM python:3.10

COPY ./financial /usr/local/financial
COPY requirements.txt /usr/local/financial/requirements.txt

WORKDIR /usr/local/financial

RUN pip install -r requirements.txt

CMD ["python", "app.py"]
 