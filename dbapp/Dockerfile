FROM python:3.12.14-slim

WORKDIR /myapp

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5001

CMD ["python", "app.py"]
