FROM ubuntu:18.04
RUN apt-get update
RUN apt-get install -y python3.10 python3-pip
RUN apt-get install -y build-essential libssl-dev libffi-dev python-dev
RUN apt-get install -y libreoffice
WORKDIR /code
COPY dev.txt requirements.txt
# RUN cat requirements.txt
RUN pip3 install --no-cache-dir --upgrade -r requirements.txt
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]


