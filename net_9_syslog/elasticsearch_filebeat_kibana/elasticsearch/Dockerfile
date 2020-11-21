# FROM elastic/elasticsearch:7.9.1
FROM harbor.qytang.com/public/elasticsearch:7.9.1
USER root
RUN /bin/cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime &&\
    echo 'Asia/Shanghai' >/etc/timezone
COPY elasticsearch.yml /usr/share/elasticsearch/config/elasticsearch.yml
COPY jvm.options /usr/share/elasticsearch/config/jvm.options