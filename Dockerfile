FROM python:3.12-alpine3.18
LABEL maintainer="arbz.92"


ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./scripts /scripts
COPY ./app /app
WORKDIR /app
EXPOSE 8000

ARG DEV=false
# linux-headers is required to install uwsgi
# zlib and zlib-dev is required to install pillow
# build-base postgresql-dev musl-dev  is required to install psycopg2
#  In most Unix-like systems, when a user is created, a corresponding primary group with the same name as the user is also created by default.
# p flag (parent) used to create nested directories which means if it is exists, no error neither overide. also / means root directory not app directory.
# in the following chown command, the first instance represents the username, and the second instance represents the group name
# it'll have permission to make changes to directory when we're running our app.
# if we don't assign django-user to it, then they're going to be created under the root user and then when we run our application in the django-user, we're not going to be able to access the directory to make changes.
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client jpeg-dev && \
    apk add --update --no-cache --virtual .tmp-build-deps \
        build-base postgresql-dev musl-dev zlib zlib-dev linux-headers && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ $DEV = "true" ]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    rm -rf /tmp && \
    apk del .tmp-build-deps && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user && \
    mkdir -p /vol/web/media && \
    mkdir -p /vol/web/static && \
    chown -R django-user:django-user /vol && \
    chmod -R 755 /vol && \
    chmod -R +x /scripts   # x=executable

#     7 (Read + Write + Execute) for the owner.
#     5 (Read + Execute) for the group.
#     5 (Read + Execute) for others.

# In Unix-like systems, including Linux and macOS, the colon (:) character is commonly used as a delimiter to separate multiple paths in environment variables or command-line arguments.
# This sets the PATH environment variable to include two directories (/scripts and /py/bin) followed by the existing PATH value ($PATH).
ENV PATH="/scripts:/py/bin:$PATH"

# whatever user is the last user to switch to when we're building our docker image will be the user that is used to run the application.
USER django-user

# this line execute when container starts and is actually 'sh ../scripts/run.sh' but if you have a shebang in your script and change its executable mode then you do not need to use sh, also if you add scripts directory to environment variable then you do not need to use full path.
CMD ["run.sh"]
