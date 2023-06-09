FROM astj/centos5-vault

COPY ["crontab.txt", "start.sh", "/"]

RUN sed -i 's?vault.centos.org?mirrors.aliyun.com/centos-vault?g' /etc/yum.repos.d/*.repo \
    && yum install -y epel-release \
    && yum clean all \
    && yum -y update \
    && yum makecache \
    && yum install -y glibc.i686 libstdc++.so.6 openssl net-tools vixie-cron passwd \
    && cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
    && useradd c7mon \
    && cat /crontab.txt > /var/spool/cron/c7mon \
    && yum clean all \
    && rm -rf /tmp/* \
    && rm -rf /var/cache/*

ENTRYPOINT ["/bin/bash", "start.sh"]

