FROM python:3.12
RUN apt-get update
RUN apt-get install -y \
  dos2unix \
  libpq-dev \
  libmariadb-dev-compat \
  libmariadb-dev \
  gcc
WORKDIR ./service
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONNUNBUFFED 1
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .