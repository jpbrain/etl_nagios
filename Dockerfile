FROM python:3

WORKDIR /usr/src/app
RUN mkdir -p output
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./nagiosdata.py" ]