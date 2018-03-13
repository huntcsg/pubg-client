FROM python:3.6.3-slim

RUN apt-get update -y && \
    apt-get install -y git-all && \
    git config --global user.name "pubg-client-deploy" && \
    git config --global user.email "huntcsg@gmail.com"

WORKDIR /package
COPY dev_requirements.txt ./
RUN pip install -r dev_requirements.txt
COPY . ./

RUN pip install .[dev]

ENTRYPOINT [ "./bin/manage_entrypoint" ]