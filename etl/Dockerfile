FROM python:3.10

RUN apt-get update && apt-get install -y python3 python3-pip
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
WORKDIR /usr/src

COPY ./requirements.txt .

RUN pip install --upgrade pip &&  \
    pip install --no-cache-dir -r requirements.txt

COPY . /usr/src/etl

ENV PYTHONPATH "${PYTHONPATH}:/usr/src"

CMD ["python", "etl/etl_process_data.py"]