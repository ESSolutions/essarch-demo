FROM centos:7

RUN curl --silent --location https://rpm.nodesource.com/setup_8.x | bash -
RUN curl --silent --location https://dl.yarnpkg.com/rpm/yarn.repo | tee /etc/yum.repos.d/yarn.repo

RUN yum install https://centos7.iuscommunity.org/ius-release.rpm -y \
    && yum update -y \
    && yum install -y git nodejs yarn gcc cairo pango python36u python36u-devel python36u-pip bzip2 \
    && yum clean all
RUN yarn global add gulp

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
