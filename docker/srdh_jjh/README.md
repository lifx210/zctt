# zctt for shanghai ChinaMobile
依赖 centos5 版本系统制作 srdh_jjh 程序运行环境

# docker run
docker run \
-itd \
--name c1 \
-v /zctt/srdh/8221/c7mon:/home/c7mon \
-v /zctt/srdh/8221/sybase-12.5:/home/sybase-12.5 \
zctt/srdh_jjh

