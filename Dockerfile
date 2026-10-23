FROM python:3.12-alpine

WORKDIR /app

# copies EVERYTHING into the image - including the .env file and the .git folder
COPY . .

RUN pip install -r requirements.txt

EXPOSE 8000

# no USER line: the app runs as root
CMD ["python", "app.py"]
