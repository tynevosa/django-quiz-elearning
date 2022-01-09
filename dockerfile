# syntax=docker/dockerfile:1
FROM python:3.9

## Activate virtual env if needed
# ENV VIRTUAL_ENV=/opt/venv
# RUN python -m venv $VIRTUAL_ENV
# ENV PATH="$VIRTUAL_ENV/bin:$PATH"
##


ENV PYTHONPATH "${PYTHONPATH}:/app"
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt /app/
RUN pip install -r requirements.txt
RUN django-admin startproject elearning ./; exit 0
COPY . /app/

# Install Nodejs
RUN apt-get update \
  && apt-get install -y build-essential curl \
  && curl -sL https://deb.nodesource.com/setup_14.x | bash - \
  && apt-get install -y nodejs --no-install-recommends \
  && rm -rf /var/lib/apt/lists/* /usr/share/doc /usr/share/man \
  && apt-get clean 

# Install Tailwind
RUN python manage.py tailwind install --no-input;
RUN python manage.py tailwind build --no-input;
RUN python manage.py collectstatic --no-input;
