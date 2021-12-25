FROM python:3.9.2
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PORT 80
WORKDIR /app


COPY ./requirements.txt .
RUN pip install -r requirements.txt
COPY . .
RUN chmod +x ./utils/run.sh
RUN ln -s /run/shm /dev/shm

# add and run as non-root user
RUN adduser --disabled-password django
USER django


WORKDIR /app

EXPOSE $PORT
ENTRYPOINT ["utils/run.sh"]
