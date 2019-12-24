FROM python:3.7.2-slim

RUN apt-get update && apt-get install -y \
		gcc \
		gettext \
		mysql-client default-libmysqlclient-dev \
		sqlite3 \
	--no-install-recommends && rm -rf /var/lib/apt/lists/*

ENV PYTHONUNBUFFERED 1
RUN mkdir /app

COPY ./ /app
WORKDIR /app

# RUN pip install --upgrade pip
# RUN pip install pipenv
RUN pip install -r requirements.txt

RUN python manage.py makemigrations
RUN python manage.py migrate
# RUN pipenv install
EXPOSE 8000
#Run Server
# ENTRYPOINT ["./entrypoint.sh"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
# define the default command to run when starting the container
# CMD ["gunicorn", "--bind", ":8000", "knit_server.wsgi"]