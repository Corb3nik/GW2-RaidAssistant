from python:3.9.1-slim

RUN mkdir /app
COPY requirements.txt /app/requirements.txt
RUN pip3 install -r /app/requirements.txt

WORKDIR /app
COPY src .

CMD ["python3", "raid_assistant.py"]

