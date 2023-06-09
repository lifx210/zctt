# zctt for shanghai ChinaMobile
依赖 openEuler 22.03 系统制作 DMPP 程序运行环境

# docker 运行
docker run \
-itd \
--name c1 \
--net=host \
-v /zctt/dmpp/dmp/:/zctt/dmp/ \
-v /dmpdata1:/dmpdata1 \
-v /dmpdata2:/dmpdata2 \
-v /dmpdata3:/dmpdata3 \
-v /dmpdata4:/dmpdata4 \
dmpp/ol
