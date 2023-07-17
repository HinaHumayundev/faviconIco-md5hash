FROM python:3.11.1-bullseye
ADD . /app
WORKDIR /app
RUN pip install -r requirements/requirements.txt
RUN pip install pytest

# Copy the application code into the container
COPY . .

# Expose the port on which the FastAPI app will run
WORKDIR /app/src
EXPOSE 8000

# Start the FastAPI app with Uvicorn server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
