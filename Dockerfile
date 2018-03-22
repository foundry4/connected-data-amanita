FROM gcr.io/bbc-connected-data/microservice-base

# Copy the application over into the container.
ADD . $APP_PATH

# Install  the application's dependencies.
RUN pip3 install -r $APP_PATH/requirements.txt

#set env vars
ENV GUNICORN_MODULE=app.api
ENV GUNICORN_CALLABLE=app
ENV GUNICORN_PORT=5000
