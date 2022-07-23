FROM python:3.8


RUN pip install pipenv
WORKDIR /code
COPY Pipfile.lock .
RUN pipenv sync --system


CMD ["python", "main.py"]
