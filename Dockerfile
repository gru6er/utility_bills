FROM python:alpine3.19
WORKDIR	/app
COPY . .
RUN pip3 install --no-cache-dir -r requirements.txt 
RUN adduser -DH abc && chown -R abc:abc /app
USER abc
CMD [ "python", "./bot.py" ]


