FROM python:3.11

WORKDIR /app

COPY lab1/producer/requirements.txt .

RUN pip install -r requirements.txt

COPY lab1/producer/producer-ferlab.py .

CMD ["python", "producer-ferlab.py"]