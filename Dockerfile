
FROM python:3.13.2

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir -r /code/requirements.txt

COPY . /code/

# ENV_VARS를 빌드 타임 인자로 받아서 .env 파일로 저장
ARG ENV_VARS
RUN echo "$ENV_VARS" | base64 -d > /code/.env

EXPOSE 80

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
