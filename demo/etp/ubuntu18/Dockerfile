FROM ubuntu:18.04

RUN apt-get update && \
    apt-get -y remove cmdtest yarn && \
    apt-get install -y python3.6 python3-pip python3.6-dev python3-cairocffi git nodejs npm pango1.0-tests postgresql-client libmariadbclient-dev

RUN npm install -g yarn && yarn global add gulp

ENV EC /src/ess_core
ENV ESS_CONFIGS /src/ess_configs
ENV ETP_ROOT /src/etp
ENV ETP $ETP_ROOT/ESSArch_TP
ENV EC_FRONTEND $EC/ESSArch_Core/frontend
ENV PYTHONPATH $PYTHONPATH:$ETP:$EC:$ESS_CONFIGS
ENV DJANGO_SETTINGS_MODULE config.settings

EXPOSE 8000

WORKDIR $ETP_ROOT

RUN git clone https://github.com/ESSolutions/ESSArch_Tools_Producer.git --depth=1 $ETP_ROOT
RUN git clone https://github.com/ESSolutions/ESSArch_Core.git --depth=1 $EC

ADD demo/etp/bootstrap.sh .
RUN ./bootstrap.sh

ADD . /src/ess_configs/

CMD /bin/bash -c "$ESS_CONFIGS/demo/etp/runtime_config.sh && python ESSArch_TP/manage.py runserver 0.0.0.0:8000"
