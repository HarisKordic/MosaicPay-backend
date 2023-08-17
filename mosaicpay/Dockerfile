# Use an official Python runtime as the base image
FROM python:3.11

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install the dependencies
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory into the container at /app
COPY . /app

# Set the environment variable for Django
ENV DJANGO_SETTINGS_MODULE=mosaicpay.settings

# Expose the port the Django app runs on
EXPOSE 8000

# Define the command to run your app
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
