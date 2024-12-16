FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /myproject

# Copy Pyproject file
COPY ./pyproject.toml .
COPY ./requirements.txt .
COPY ./.env .

# Install dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY . .

# Collect static files
RUN python3 manage.py collectstatic --noinput

# Expose the port
EXPOSE 8000

# Run the application
ENTRYPOINT ["sh", "-c", "python3 manage.py migrate && python3 manage.py runserver 0.0.0.0:8000"]
