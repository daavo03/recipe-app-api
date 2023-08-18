FROM python:3.9-alpine3.13
LABEL maintener="daavo"

# It tells python that you don't want to buffer the output.
# The output from python will be printed directly to the console which prevents any delays 
ENV PYTHONUNBUFFERED 1


COPY ./requirements.txt /tmp/requirements.txt
COPY ./app /app
WORKDIR /app
EXPOSE 8000

# This creates a new virtualenv to store our dependencies
RUN python -m venv /py && \
  # From our virtualenv we want to upgrade pip
  /py/bin/pip install --upgrade pip && \
  # Installing the python requirements in our virtualenv
  /py/bin/pip install -r /tmp/requirements.txt && \
  # We remove the tmp directory, bc we don't want extra dependencies on our image once it's created
  rm -rf /tmp && \
  # This block adds a new user inside our image to not use the root user
  adduser \
    --disabled-password \
    --no-create-home \
    django-user

# This updates the env variable inside the image. We're updating the PATH env variable
# So when we run any command in our project we dont need to specify the full path  
ENV PATH="/py/bin:$PATH"

# This specifies the user that we're switching to
USER django-user