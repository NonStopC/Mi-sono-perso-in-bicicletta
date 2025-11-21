FROM python:3.11-slim


WORKDIR /backend

COPY . /backend/

RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

EXPOSE 1234

CMD [ "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "1234" ]

