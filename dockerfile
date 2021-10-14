FROM python:3.9-slim

EXPOSE 8080

ENV SECRET_KEY=mysecret
ENV EMAIL_HOST=smtp.provider.com
ENV EMAIL_PORT=465
ENV EMAIL_HOST_USER=instodramat@provider.com
ENV EMAIL_HOST_PASSWORD=instodramat_password


ADD ./Instodramat /app
ADD ./requirements.txt /app
WORKDIR /app
RUN mkdir /app/media
RUN mkdir /app/media/Avatars

RUN pip3 install -r requirements.txt

RUN python3 manage.py makemigrations
RUN python3 manage.py migrate

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8080"]
