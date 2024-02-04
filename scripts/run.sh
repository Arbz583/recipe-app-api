#!/bin/sh

#It ensures that the script terminates as soon as any command fails, preventing the script from continuing execution in an error state.
set -e

python manage.py wait_for_db
python manage.py collectstatic --noinput
python manage.py migrate

uwsgi --socket :9000 --workers 4 --master --enable-threads --module app.wsgi

# It listens for incoming requests on port 9000.
# It spawns 4 worker processes to handle incoming requests.
# It enables the master process to manage the worker processes.
# It enables support for multithreading within each worker process.
# It serves the WSGI application defined in the app.wsgi module that is entry point for our project.
# The app.wsgi module is responsible for creating the WSGI application object, which is typically named application. This object is responsible for handling incoming HTTP requests and generating responses. When uWSGI loads the specified module using the --module option, it expects to find this application object, which it will then serve to handle incoming requests.
# while the WSGI application object handles the core logic of processing HTTP requests and generating responses, uWSGI provides the infrastructure and mechanisms for scalability, concurrency, and fault tolerance to ensure the smooth operation of WSGI-based web applications.
# while you can use Nginx directly with WSGI applications without a separate WSGI server (such as uwsgi), you still need Nginx to act as a reverse proxy to forward requests to your WSGI application and handle static files.
