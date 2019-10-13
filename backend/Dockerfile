FROM python:3.7 as builder
RUN mkdir /install
WORKDIR /install
RUN pip install --install-option="--prefix=/install" pipenv

# Final image:
# if slim does not work change it to python:3.7
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7
RUN apt-get update --fix-missing

ENV PYTHONUNBUFFERED 1
EXPOSE 8888
# getting requirements from base image
COPY --from=builder /install /usr/local
COPY ./crts/root.crt /root/.postgresql/root.crt
# copying source files into app folder of container
COPY ["Pipfile", "Pipfile.lock", "ospackages.txt", "./"]
# install system dependencies from ospackages.txt
RUN cat ospackages.txt | xargs apt-get install -y
# installing requirements.txt with pipenv
RUN pipenv install --system --deploy
RUN mkdir -p /tmp/prometheus_multiproc_dir/
COPY ./src /app
WORKDIR /app
ENV PYTHONPATH=/app