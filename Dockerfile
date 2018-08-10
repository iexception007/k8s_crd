FROM python:2.7-alpine

#RUN mkdir -p /opt/code/crd_helper
COPY . /opt/code/crd_helper

RUN mkdir -p ~/.pip
RUN mv /opt/code/crd_helper/config/pip.conf ~/.pip/

WORKDIR /opt/code/crd_helper
RUN pip install -r requirements.txt

CMD python ./crd_helper.py
