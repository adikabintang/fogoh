FROM adikabintang/python-opencv-alpine:alp3.9-py3.7-ocv4.1
RUN apk add wget make
RUN pip install --no-cache-dir uvloop
RUN pip install --no-cache-dir asyncio-nats-client==0.8.2 asyncio-nats-streaming==0.2.0
WORKDIR /usr/src/app
COPY . .
RUN ./get_models.sh
RUN apk del wget make
CMD [ "python", "-u", "./main.py" ]