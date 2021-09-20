FROM python:3-alpine

# Add your instructions to dockerize the application
# App must run on port 8000

WORKDIR /capstone-project

ADD . /app

EXPOSE 8000/tcp

RUN pip install -r /app/requirements.txt

CMD ["python", "/app/api.py"]