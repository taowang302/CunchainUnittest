# CunchainUnittest
## 说明：脚本基于python3编写

## 环境准备
### 安装python3

yum install -y epel-release

yum install -y python34

### 安装pip3

wget --no-check-certificate https://bootstrap.pypa.io/get-pip.py

python3 get-pip.py

### 安装第三方库

pip3 install requests

pip3 install ConfigParser

pip3 install mysql-connector

## 运行方式
脚本使用两种运行方式
### 脚本方式运行
    1、 正确配置配置文件
    2、 运行script 下main.py  python main.py
    
### 启动server进程，开放API接口
    1、正确配置配置文件
    2、两种方式启动app下app.py 
        a) python3 app.py ## 启动在前台
        b) python3 app.py -d ## 启动到后台