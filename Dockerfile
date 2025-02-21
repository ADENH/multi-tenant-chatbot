FROM python:3.9
WORKDIR /app
COPY . .
# Upgrade pip and install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Explicitly install OpenAI library
RUN pip install openai

# Explicitly install uvicorn
RUN pip install fastapi uvicorn

# Set the default command to run the FastAPI app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
