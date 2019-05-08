FROM python:3.7.3-alpine3.9
RUN pip install --no-cache-dir asyncio-nats-client==0.8.2 \
    asyncio-nats-streaming==0.2.0 \
    uvloop Pillow protobuf
WORKDIR /usr/src/app
COPY main.py ./
CMD [ "python", "./main.py" ]