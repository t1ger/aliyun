
Base on alislb https api,modify aliyun slb

命令行解析阿里云 SLB
首先需要获取阿里云账号账号的AccessKeyID及AccessKeySecret，并将其替换至 alislb.py 文件中

然后安装阿里云的接口

#pip install aliyun-python-sdk-core-v3

#pip install aliyun-python-sdk-slb
使用说明：

[root@localhost]# ./alislb.py -h
usage: alislb.py [-h] [-a | -d | -u | -g]

              instance ip weight [instance ip weight ...]

针对 SLB INSTANC 进行相关操作

positional arguments:

   instance ip weight  实例 IP 权重

optional arguments:

    -h, --help           show this help message and exit
  
    -a, --add            add ecs. (e.g. --add instance ip weight)
  
    -d, --delete         delete ecs. (e.g. --delete instance ip)
  
    -u, --update         update ecs info. (e.g. --update instance ip weight)
  
    -g, --get            get slb info,default all. (e.g. --get instance)


增加主机 ./alislb.py -a instance ip  weight

更新解析 ./alislb.py -u instance ip  weight

获取解析 ./alislb.py -g instance

删除解析 ./alislb.py -d instance ip

