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
    log_level = level_dic.get(log_level.upper())
    # log_level = log_level.upper()
    # 创建一个logger
    logger = logging.getLogger('runlog')
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


def config_db_log(config):
    logger = logging.getLogger('debugdblog')
    logger.setLevel(logging.DEBUG)
    # 创建一个用于sql打印的日志线程
    fh = logging.FileHandler(config.get('log_path'))
    # fh = logging.StreamHandler()
    # print(config.get('debug_db_log'))
    if 'TRUE' == config.get('debug_db_log').upper():
        fh.setLevel(logging.DEBUG)
    else:
        fh.setLevel(logging.WARNING)
    formatter = logging.Formatter(
        "[%(asctime)s] [debugdb] %(levelname)s [TD%(thread)d] %(message)s",
        datefmt='%F %T')
    if 'TRUE' == config.get('console_log').upper():
        ch = logging.StreamHandler()
        if 'TRUE' == config.get('debug_db_log').upper():
            ch.setLevel(logging.DEBUG)
        else:
            ch.setLevel(logging.WARNING)
        ch.setFormatter(formatter)
        # 给logger添加handler
        logger.addHandler(ch)
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger


if __name__ == '__main__':
    dblog = config_db_log({
        "log_level": "debug",
        "debug_db_log": "true",
        "log_path": "../log/unittest.log",
        "console_log": 'true'
    })
    log = config_log({
        "log_level": "debug",
        "debug_db_log": "true",
        "log_path": "../log/unittest.log",
        "console_log": 'true'
    })

    log.info('test for runlog')
    dblog.info('test for dbebug db log')
