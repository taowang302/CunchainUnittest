import logging


def config_log(config_file):
    log_level = config_file.get("log_level")
    log_level = log_level.upper()
    level_dic = {"DEBUG": logging.DEBUG, "INFO": logging.INFO, "ERROR": logging.ERROR, "CRITICAL": logging.CRITICAL,
             "WARNING": logging.WARNING}
    logging.basicConfig(level=level_dic.get(log_level),format='[%(asctime)s] [%(module)s] [%(lineno)d] %(funcName)s %(levelname)s [TD%(thread)d] %(message)s',datefmt='%F %T')
    return logging

