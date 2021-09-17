# BUILD UI
FROM node:14-alpine
WORKDIR ./src
COPY ./invites_app_ui .

RUN yarn install
RUN yarn build --config webpack.$BUILD_ENV.js --mode $BUILD_ENV

# BUILD APP
FROM python:3.8-bullseye

ADD . /application

WORKDIR application

# COPY UI BUNDLE FROM STAGE_1
RUN mkdir /opt/data
RUN mkdir /opt/data/static
RUN mkdir ./src/bp_images
COPY --from=0 /src/dist/ /opt/data/static/
RUN rm -rf ./invites_app_ui

RUN apt-get update && apt-get install -y nginx

RUN python -m pip install --upgrade pip
RUN pip install pipenv

RUN pipenv install --system --deploy --ignore-pipfile

EXPOSE 8000

ENTRYPOINT uvicorn --host 0.0.0.0 --port 8000 src.app.main:app;
