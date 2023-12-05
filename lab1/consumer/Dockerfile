FROM python:3.11

WORKDIR /app

COPY lab1/consumer/requirements.txt .

RUN pip install -r requirements.txt

COPY lab1/consumer/consumer-ferlab.py .

CMD ["python", "consumer-ferlab.py"]