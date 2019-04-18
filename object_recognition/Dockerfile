FROM adikabintang/python-opencv-alpine:alp3.9-py3.7-ocv4.1
RUN pip install --no-cache-dir uvloop
RUN pip install --no-cache-dir asyncio-nats-client==0.8.2 asyncio-nats-streaming==0.2.0
WORKDIR /usr/src/app
COPY . .
RUN ./get_models.sh
CMD [ "python", "-u", "./main.py" ]