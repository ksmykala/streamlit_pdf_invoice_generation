FROM python:3.10-slim

WORKDIR /app

# Install dependencies required for WeasyPrint and libgobject
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libffi-dev \
    libcairo2 \
    libjpeg62-turbo \
    libpng-dev \
    libharfbuzz-bin \
    shared-mime-info \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "streamlit_app.py", "0.0.0.0", "--server.port=8501", "--server.address=0.0.0.0"]