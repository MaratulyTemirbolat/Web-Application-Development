FROM python:3.12-slim

# Set the working directory
WORKDIR /myproject

# Copy Pyproject file
COPY ./pyproject.toml .
COPY ./requirements.txt .

# Install dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY . .

# Make migrations
RUN python3 manage.py makemigrations

# Apply migrations
RUN python3 manage.py migrate

# Expose the port
EXPOSE 8000

# Run the application
ENTRYPOINT ["python3", "manage.py", "runserver"]
