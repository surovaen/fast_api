FROM python:3.10-slim


COPY . /fast_api
WORKDIR /fast_api
RUN pip install --upgrade pip
COPY . /requirements.txt
RUN pip install -q -r requirements.txt
CMD ["bash", "./entrypoint.sh"]
