import logging
import configparser


def config_log(config_file，


    logconfig):
    config = configparser.ConfigParser()
    config.read(config_file)
log_level = config['LOG'][logconfig]
    log_level = log_level.upper()
if "TRUE" == logconfig:
    log_level = "DEBUG"
elif "FALSE" == logconfig:
    log_level = "WARNING"
level_dic = {"DEBUG": logging.DEBUG, "INFO": logging.INFO, "ERROR": logging.ERROR, "CRITICAL": logging.CRITICAL,
             "WARNING": logging.WARNING}
    logging.basicConfig(level=level_dic.get(log_level),format='[%(asctime)s] [%(module)s] [%(lineno)d] %(funcName)s %(levelname)s [TD%(thread)d] %(message)s',datefmt='%F %T')
    return logging


if __name__ == "__main__":
    log = config_log("../conf/global_config.ini")
    log.error("test")
