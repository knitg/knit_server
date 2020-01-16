FROM python:3.7.2-slim

# arbitrary location choice: you can change the directory
RUN mkdir -p /opt/services/djangoapp/src
# WORKDIR /opt/services/djangoapp/src

RUN apt-get update && apt-get install -y \
		gcc \
		gettext \
		mysql-client default-libmysqlclient-dev \
		sqlite3 \
	--no-install-recommends && rm -rf /var/lib/apt/lists/*

ENV PYTHONUNBUFFERED 1

# copy our project code
# COPY . /opt/services/djangoapp/src
COPY ./app /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 8000
# CMD ["gunicorn", "--bind", ":8000", "knit_server.wsgi"]