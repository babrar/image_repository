From python:3.9

WORKDIR /app

COPY . /app/
RUN python3 -m pip install -r requirements.txt

EXPOSE 5000

CMD [ "python3", "wsgi.py" ]