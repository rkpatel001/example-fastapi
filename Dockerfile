FROM python:3.12

WORKDIR /user/src/app

COPY requirements.txt ./

RUN pip install -r requirements.txt

# Ensure uvicorn is installed
RUN pip install uvicorn fastapi

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]













