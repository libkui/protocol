# FROM elastic/filebeat:7.9.1
FROM harbor.qytang.com/public/filebeat:7.9.1
USER root
RUN /bin/cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime &&\
    echo 'Asia/Shanghai' >/etc/timezone
RUN rm /usr/share/filebeat/modules.d/cisco.yml.disabled
COPY cisco.yml /usr/share/filebeat/modules.d/cisco.yml
COPY filebeat.yml /usr/share/filebeat/filebeat.yml