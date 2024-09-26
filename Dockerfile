FROM python:3.9.20-alpine3.20

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt requirements.txt

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY static ./static
COPY app.py app.py

# Run app.py when the container launches
CMD ["python", "app.py"]