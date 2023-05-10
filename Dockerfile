FROM python:3.11.3
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install --upgrade setuptools
RUN pip3 install -r requirements.txt
COPY