#
FROM python:3.9

#
WORKDIR /App

#
COPY ./requirements.txt /App/requirements.txt

#
RUN pip install --no-cache-dir --upgrade -r /App/requirements.txt

#
COPY ./app /App/app

#
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]