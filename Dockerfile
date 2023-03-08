FROM python:3.11.2-slim-buster
WORKDIR /code/
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY . /code/
CMD python -m pytest; python app/main.py