# FROM elastic/kibana:7.9.1
FROM harbor.qytang.com/public/kibana:7.9.1
USER root
RUN /bin/cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime &&\
    echo 'Asia/Shanghai' >/etc/timezone
COPY kibana.yml /usr/share/kibana/config/kibana.yml
COPY node.options /usr/share/kibana/config/node.options
USER kibana