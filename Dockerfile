FROM python:3
MAINTAINER "Janik Luechinger janik.luechinger@uzh.ch"

COPY . /pga
WORKDIR /pga

RUN apt-get -y update && apt-get -y upgrade
RUN pip install -U pip && pip install -r requirements.txt

ENTRYPOINT [ "python", "-m", "mutation" ]

# Manual image building
# docker build -t pga-cloud-mutation .
# docker tag pga-cloud-mutation jluech/pga-cloud-mutation
# docker push jluech/pga-cloud-mutation
