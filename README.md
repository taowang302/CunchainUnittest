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

## 配置文件
    # ---------------------------------------------------------------------------------
    # config database
    # ---------------------------------------------------------------------------------
    [DATABASE]
    host = 192.168.15.171
    port = 3306
    user = root
    passwd = jbi123456
    db = unittest
    charset = utf8
    
    [RUNCASECONFIG]
    # ---------------------------------------------------------------------------------
    # Valid only when running independently
    # 0 for run those casees which id in case_id
    # 1 for run all of casees
    # ---------------------------------------------------------------------------------
    runmode = 0
    case_id = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,8,4,15,16,17]
    archive_id = f_001
    output_dir = ../html/report.html
    
    [LOG]
    # ---------------------------------------------------------------------------------
    # log_level - allowed values are: debug, info, warn, error
    # debug_db_log - allowed values are: true, false
    # console_log - allowed values are: true, false
    # true for write log to file and console
    # false for write log to file only
    # ---------------------------------------------------------------------------------
    log_level = info
    debug_db_log = false
    log_path = ../log/unittest.log
    console_log = true
    
    [SERVER]
    # ---------------------------------------------------------------------------------
    #  Valid only when run webserver
    # ---------------------------------------------------------------------------------
    ipaddr =
    listen_port = 8088
    output_dir = ../html/eport.html




## 运行方式
脚本使用两种运行方式
### A、脚本方式运行
    1、 正确配置配置文件
    2、 运行script 下main.py  python main.py
    
### B、启动server进程，开放API接口
    1、正确配置配置文件
    2、两种方式启动app下app.py 
        a) python3 app.py ## 启动在前台
        b) python3 app.py -d ## 启动到后台

## API 说明
### 1、获取用例信息

request:

    {
    "method": "get_info"
    }

reponse:

    {
        "status": "success",
        "total_nu": 2,
        "data": [
            {
                "arhive_id": "f_002",
                "case_nu": 0,
                "description": "the first version for cunchain"
            },
            {
                "arhive_id": "f_001",
                "case_nu": 24,
                "description": "the second version for cunchain"
            }
        ]
    }


### 2、获取用例详细信息

request:
    
    {
        "method": "get_case_info",
        "data": "f_001"
    }
    
reponse:

    {
        "status": "success",
        "total": 24,
        "data": [
            {
                "case id": "9",
                "api": "/api/v0/user/login",
                "method": "GET",
                "description": "login"
            },
            {
                "case id": "5",
                "api": "/api/v0/user/info",
                "method": "GET",
                "description": "info"
            },
            {
                "case id": "",
                "api": "/api/v0/finance/list",
                "method": "GET",
                "description": "info"
            },
            {
                "case id": "2",
                "api": "/api/v0/captcha/sms",
                "method": "GET",
                "description": null
            },
            {
                "case id": "16",
                "api": "/api/v0/status/entry",
                "method": "GET",
                "description": "get entry info"
            },
            {
                "case id": "",
                "api": "/api/v0/transfer/token",
                "method": "GET",
                "description": "transfer token"
            },
            {
                "case id": "17",
                "api": "/api/v0/hash/load",
                "method": "GET",
                "description": "load hash"
            },
            {
                "case id": "15",
                "api": "/api/v0/hash/save",
                "method": "GET",
                "description": "save hash"
            },
            {
                "case id": "6",
                "api": "/api/v0/user/update",
                "method": "GET",
                "description": "update account information"
            },
            {
                "case id": "",
                "api": "/api/v0/pay_token/create",
                "method": "GET",
                "description": "create qr code and address for token payment"
            },
            {
                "case id": "",
                "api": "/api/v0/pay_wx/create",
                "method": "GET",
                "description": null
            },
            {
                "case id": "",
                "api": "/api/v0/pay_wx/check",
                "method": "GET",
                "description": null
            },
            {
                "case id": "",
                "api": "/api/v0/proof/list",
                "method": "GET",
                "description": null
            },
            {
                "case id": "",
                "api": "/api/v0/qr/image",
                "method": "GET",
                "description": null
            },
            {
                "case id": "12",
                "api": "/api/v0/transfer/credit",
                "method": "GET",
                "description": null
            },
            {
                "case id": "13",
                "api": "/api/v0/transfer/token",
                "method": "GET",
                "description": null
            },
            {
                "case id": "7",
                "api": "/api/v0/upload/img",
                "method": "POST",
                "description": null
            },
            {
                "case id": "8",
                "api": "/api/v0/user/logout",
                "method": "GET",
                "description": "user logout"
            },
            {
                "case id": "3",
                "api": "/api/v0/user/register",
                "method": "GET",
                "description": "register new user account"
            },
            {
                "case id": "1",
                "api": "/api/v0/captcha/image",
                "method": "GET",
                "description": null
            },
            {
                "case id": "4",
                "api": "/api/v0/user/login",
                "method": "GET",
                "description": "login"
            },
            {
                "case id": "10",
                "api": "/api/v0/org/user/info",
                "method": "GET",
                "description": null
            },
            {
                "case id": "11",
                "api": "/api/v0/org/user/update",
                "method": "POST",
                "description": "update account information in my organization"
            },
            {
                "case id": "14",
                "api": "/api/v0/org/user/finance/list",
                "method": "GET",
                "description": null
            }
        ]
    }

### 3、运行用例

request:

    {
        "method": "run_case",
        "data": {
            "archiveid": "f_001",
            "case_list": [ 1,2,3,13 ]
        }
    }  
        
reponse:

    {
        "status": "success",
        "data": {
            "case_total": 4,
            "success_nu": 0,
            "fail_nu": 0,
            "err_nu": 1,
            "report_url": "../html/report20170911164111.html"
        }
    }


