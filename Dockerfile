FROM python:3.10

 
WORKDIR /code

 
RUN git clone https://github.com/ItsBubbles/kupple.git && cd kupple && git pull && git checkout yadig-build

COPY requirements.txt /tmp/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /tmp/requirements.txt
 
COPY ./app /code/app
COPY ./data /code/data

EXPOSE 8091

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8091"]
