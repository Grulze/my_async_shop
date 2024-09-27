FROM python:3.11-alpine

RUN mkdir /items

WORKDIR /items

COPY . .

RUN pip install -r requirements.txt

CMD ["uvicorn", "main:my_shop", "--host", "0.0.0.0", "--port", "8000"]