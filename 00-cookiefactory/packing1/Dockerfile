FROM arm64v8/python:alpine

RUN pip3 install requests
RUN pip3 install Flask

EXPOSE 8000 80

COPY . .

CMD ["/usr/local/bin/python", "/main.py"]