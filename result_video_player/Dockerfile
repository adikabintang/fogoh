FROM jjanzic/docker-python3-opencv:opencv-4.0.1
RUN pip install --no-cache-dir asyncio-nats-client==0.8.2 asyncio-nats-streaming==0.2.0
WORKDIR /usr/src/app
COPY main.py ./
CMD [ "python", "./main.py" ]