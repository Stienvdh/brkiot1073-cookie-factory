FROM arm64v8/python:alpine

RUN pip3 install pyserial
RUN pip3 install requests
RUN pip3 install Flask
RUN pip3 install smbus2

EXPOSE 5000

COPY . .

CMD ["/usr/local/bin/python", "/main.py"]