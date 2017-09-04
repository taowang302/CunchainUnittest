import logging


# def config_log(config_file):
#     log_level = config_file.get("log_level")
#     log_level = log_level.upper()
#     level_dic = {"DEBUG": logging.DEBUG, "INFO": logging.INFO, "ERROR": logging.ERROR, "CRITICAL": logging.CRITICAL,
#              "WARNING": logging.WARNING}
#     logging.basicConfig(level=level_dic.get(log_level),
#                         format='[%(asctime)s] [%(module)s] [%(lineno)d] %(funcName)s %(levelname)s [TD%(thread)d] %(message)s',
#                         datefmt='%F %T',
#                         filename=config_file.get('log_path'),
#                         filemode='a')
#     return logging


# import logging

def config_log(config):
    level_dic = {"DEBUG": logging.DEBUG,
                 "INFO": logging.INFO,
                 "ERROR": logging.ERROR,
                 "CRITICAL": logging.CRITICAL,
                 "WARNING": logging.WARNING}
    log_level = config.get("log_level")
    log_level = log_level.upper()
    # 创建一个logger
    logger = logging.getLogger()
    logger.setLevel(log_level)
    # 定义handler的输出格式
    formatter = logging.Formatter(
        "[%(asctime)s] [%(module)s] [%(lineno)d] %(funcName)s %(levelname)s [TD%(thread)d] %(message)s",
        datefmt='%F %T')

    # 创建一个handler，用于写入日志文件
    fh = logging.FileHandler(config.get('log_path'))
    fh.setLevel(log_level)
    fh.setFormatter(formatter)
    # 给logger添加handler
    logger.addHandler(fh)
    # 再创建一个handler，用于输出到控制台
    if 'TRUE' == config.get('console_log').upper():
        ch = logging.StreamHandler()
        ch.setLevel(log_level)
        ch.setFormatter(formatter)
        # 给logger添加handler
        logger.addHandler(ch)
    return logger


if __name__ == '__main__':
    log = config_log({
        "log_level": "debug",
        "debug_db_log": "true",
        "log_path": "../log/unittest.log",
        "console_log": 'true'
    })

    log.info('test')
