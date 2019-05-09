# Using lightweight alpine image
FROM python:3.6-alpine

# Installing packages
RUN apk update

# RUN pip install --no-cache-dir pipenv

# ADD . /urs/src/app
# Defining working directory and adding source code
WORKDIR /usr/src/app
COPY requirements.txt ./

# Install API dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Add application code.
COPY . ./

# Start app
EXPOSE 8080
CMD ["python", "app.py"]