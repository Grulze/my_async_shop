FROM python:3.11-alpine

RUN mkdir /items

WORKDIR /items

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "core.main:my_shop", "--host", "0.0.0.0", "--port", "8000"]