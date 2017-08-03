import logging
import configparser


def config_db_log(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)
    if_debug = config['LOG']['debug_db_log']
    if "TRUE" == if_debug:
        log_level = "DEBUG"
    else:
        log_level = "WARNING"
    level_dic = {"DEBUG": logging.DEBUG, "INFO": logging.INFO, "ERROR": logging.ERROR, "CRITICAL": logging.CRITICAL,
                 "WARNING": logging.WARNING}
    logging.basicConfig(level=logging.DEBUG,
                        format='[%(asctime)s] [%(module)s] [%(lineno)d] %(funcName)s [DEBUG DB LOG] %(message)s',
                        datefmt='%F %T')
    return logging
