# 指定基础镜像
FROM openeuler/openeuler

# 定义变量
ENV username=xxx
ENV userpwd=xxx
ENV adminpwd=xxx
ENV dmpPath=/zctt/dmp
ENV DBHost=10.221.231.91
ENV ProxyIP=10.222.18.226

ADD ["DMPP_Support-1.0.2.tar.gz","clickhouse.tar.gz", "/"]

RUN  mv /etc/yum.repos.d/openEuler.repo /etc/yum.repos.d/openEuler.repo.bak \
    && touch /etc/yum.repos.d/openEuler.repo \
    && echo "[everything]" >> /etc/yum.repos.d/openEuler.repo \
    && echo "name=everything" >> /etc/yum.repos.d/openEuler.repo \
    && echo "baseurl=http://${ProxyIP}/" >> /etc/yum.repos.d/openEuler.repo \
    && echo "enabled=1" >> /etc/yum.repos.d/openEuler.repo \
    && echo "gpgcheck=1" >> /etc/yum.repos.d/openEuler.repo \
    && echo "gpgkey=http://${ProxyIP}/RPM-GPG-KEY-openEuler" >> /etc/yum.repos.d/openEuler.repo \
    && dnf clean all \
    && dnf makecache \
    && dnf -y install shadow-utils passwd util-linux python libncurses* java net-tools iputils *unixODBC* mariadb-connector-odbc --allowerasing --skip-broken \
    && echo "[monitor]" >> /etc/odbc.ini \
    && echo "Driver=MariaDB" >> /etc/odbc.ini \
    && echo "Port=3306" >> /etc/odbc.ini \
    && echo "Server=${DBHost}" >> /etc/odbc.ini \
    && echo "User=netcompass" >> /etc/odbc.ini \
    && echo "Password=netcompass@staticdb.123" >> /etc/odbc.ini \
    && echo "Database=netcompass" >> /etc/odbc.ini \
    && echo "Charset=utf8" >> /etc/odbc.ini \
    && echo "Socket=" >> /etc/odbc.ini \
    && mkdir /dmpdata{1..4} \
    && groupadd $username \
    && useradd -s /bin/bash -m -g $username -d $dmpPath $username \
    && echo $userpwd  | passwd --stdin $username \
    && echo $adminpwd | passwd --stdin root \
    && rpm -ivh --nodeps --force /clickhouse/*.rpm \
    && cd /DMPP_Support-1.0.2 \
    && python setup.py install \
    && chmod -R 755 /usr/local/lib/python3.9 \
    && rm -rf /DMPP_Support-1.0.2 \
    && rm -rf /clickhouse \
    && chown -R dmp:dmp /zctt /dmpdata* \
    && dnf clean all \
    && rm -rf /var/cache/*




