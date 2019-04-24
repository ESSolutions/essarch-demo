FROM ubuntu:18.04

RUN apt-get update && \
    apt-get -y remove cmdtest yarn && \
    apt-get install -y python3.6 python3-pip python3.6-dev python3-cairocffi git nodejs npm pango1.0-tests postgresql-client libmariadbclient-dev

RUN npm install -g yarn && yarn global add gulp

ENV EC /src/ess_core
ENV ESS_CONFIGS /src/ess_configs
ENV EPP_ROOT /src/epp
ENV EPP $EPP_ROOT/ESSArch_PP
ENV EC_FRONTEND $EC/ESSArch_Core/frontend
ENV PYTHONPATH $PYTHONPATH:$EPP:$EC:$ESS_CONFIGS
ENV DJANGO_SETTINGS_MODULE config.settings

EXPOSE 8000

WORKDIR $EPP_ROOT

RUN mkdir -p /ESSArch/log/

RUN git clone https://github.com/ESSolutions/ESSArch_EPP.git $EPP_ROOT
RUN git clone https://github.com/ESSolutions/ESSArch_Core.git $EC

RUN ln -fs /usr/bin/python3.6 /usr/bin/python
RUN python -m pip install --upgrade pip
RUN python -m pip install -e ${EC}/["tests,s3,postgres,mysql,logstash"]
RUN cd ${EPP}/frontend/static/frontend && yarn && gulp

ADD . /src/ess_configs/

CMD /bin/bash -c "$ESS_CONFIGS/demo/epp/runtime_config.sh && python ESSArch_PP/manage.py runserver 0.0.0.0:8000"
