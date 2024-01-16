# Use an official Python runtime as the base image
FROM python:3.8-slim

RUN pip install mysql-connector-python
RUN pip install python-decouple
RUN pip install python-dotenv

# Set the working directory in the container to /app
WORKDIR /app

# Copy the current directory (our Flask app) into the container at /app
COPY src /app

# Install Flask and other dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available for the app
EXPOSE 5000

# Run the command to start the Flask app
CMD ["flask", "run", "--host=0.0.0.0"]
#CMD ["python3", "app.py"]