# ************************************************************
# Sequel Pro SQL dump
# Version 4541
#
# http://www.sequelpro.com/
# https://github.com/sequelpro/sequelpro
#
# Host: 192.168.15.171 (MySQL 5.5.52-MariaDB)
# Database: unittest
# Generation Time: 2017-09-12 01:00:25 +0000
# ************************************************************


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


# Dump of table case_view
# ------------------------------------------------------------

DROP TABLE IF EXISTS `case_view`;

CREATE TABLE `case_view` (
  `from_id` varchar(128) NOT NULL COMMENT '关联用例归档id',
  `to_id` int(32) NOT NULL COMMENT '关联用例结果id',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table file_bag
# ------------------------------------------------------------

DROP TABLE IF EXISTS `file_bag`;

CREATE TABLE `file_bag` (
  `file_number` varchar(32) NOT NULL COMMENT '用例归属档案编号',
  `host` varchar(128) NOT NULL DEFAULT '' COMMENT 'base url',
  `port` int(11) DEFAULT NULL,
  `base_path` varchar(128) DEFAULT NULL,
  `description` varchar(128) DEFAULT NULL COMMENT '档案说明',
  `create_time` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `file_bag` WRITE;
/*!40000 ALTER TABLE `file_bag` DISABLE KEYS */;

INSERT INTO `file_bag` (`file_number`, `host`, `port`, `base_path`, `description`, `create_time`)
VALUES
	('f_002','192.168.15.171',80,'/api/v0','the first version for cunchain',NULL),
	('f_001','192.168.15.171',80,'/api/v0','the second version for cunchain',NULL);

/*!40000 ALTER TABLE `file_bag` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table sequence
# ------------------------------------------------------------

DROP TABLE IF EXISTS `sequence`;

CREATE TABLE `sequence` (
  `name` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `current_value` int(11) NOT NULL,
  `increment` int(11) NOT NULL DEFAULT '1',
  PRIMARY KEY (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

LOCK TABLES `sequence` WRITE;
/*!40000 ALTER TABLE `sequence` DISABLE KEYS */;

INSERT INTO `sequence` (`name`, `current_value`, `increment`)
VALUES
	('ResultSeq',0,1),
	('ViewidSeq',0,1);

/*!40000 ALTER TABLE `sequence` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table test_result
# ------------------------------------------------------------

DROP TABLE IF EXISTS `test_result`;

CREATE TABLE `test_result` (
  `view_id` varchar(32) NOT NULL DEFAULT '' COMMENT '用例归档编号',
  `case_number` varchar(32) NOT NULL COMMENT '用例编号',
  `actual_response_code` varchar(32) DEFAULT NULL COMMENT '实际返回确认码',
  `actual_response` varchar(1000) DEFAULT NULL COMMENT '实际返回结果',
  `result` varchar(128) DEFAULT NULL COMMENT '用例执行结果',
  `description` varchar(1000) DEFAULT NULL COMMENT '执行结果说明',
  `queryparameters` varchar(1000) DEFAULT NULL COMMENT '实际请求body'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table usercase
# ------------------------------------------------------------

DROP TABLE IF EXISTS `usercase`;

CREATE TABLE `usercase` (
  `case_number` int(32) DEFAULT NULL,
  `case_name` varchar(128) NOT NULL COMMENT '用例名称',
  `http_method` varchar(5) NOT NULL COMMENT '交互方式',
  `queryparameters` varchar(1000) NOT NULL COMMENT '接口所需参数',
  `from_view_id` varchar(32) NOT NULL COMMENT '用例归属档案编号',
  `description` varchar(128) DEFAULT NULL COMMENT '用例说明',
  `test_method` varchar(32) DEFAULT NULL COMMENT '测试方法',
  `except_response_code` varchar(11) DEFAULT NULL COMMENT '预期响应',
  `except_response` varchar(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `usercase` WRITE;
/*!40000 ALTER TABLE `usercase` DISABLE KEYS */;

INSERT INTO `usercase` (`case_number`, `case_name`, `http_method`, `queryparameters`, `from_view_id`, `description`, `test_method`, `except_response_code`, `except_response`)
VALUES
	(9,'/api/v0/user/login','GET','{\"user\":\"org\",\"password\":\"8969ffe739e4f97f7ad717e13eae75cfcb657e8d\"}','f_001','login','test_default_normal','200',NULL),
	(5,'/api/v0/user/info','GET','{}','f_001','get user login status','test_default_normal','200',NULL),
	(22,'/api/v0/finance/list','GET','{\"start\":0,\"count\":1,\"search\":None,\"date_from\":-1,\"date_to\":-1,\"orderby\":None,\"desc\":0,\"number\":None,\"type\":None}','f_001','get finance record list','test_default_normal','200',NULL),
	(2,'/api/v0/captcha/sms','GET','{\'phone_no\': \'137715096782\', \'captcha_image\': \'5377\', \'reason\': \'register\', \'test\': \'ture\'}','f_001','send captcha sms','test_sms_normal','200',NULL),
	(16,'/api/v0/status/entry','GET','{\"entry_hash\":\"a145e4c7f8b8f85c5d110b1fbe96cfb4c4237f7cb31cc4b653dc2c872d2cb67d\"}','f_001','get entry info','test_entry_op','200',NULL),
	(24,'/pay_token/check','GET','{\"order_no\":None}','f_001','transfer token','test_transfer_token','200',NULL),
	(17,'/api/v0/hash/load','GET','{\"limit\":1,\"file_hash\":\"0df11d7b495162fe8f26bec2202264d7594697d2937d9aa7cda2311f6f9bd54d\",\"entry_hash\":\"EC3SnieQ3DqNhC3s4W5q29Lyk4VNPGhhFQcAfPPcXZBHwegQpmmz\"}','f_001','check if file hash exists in cunchain network','test_default_normal','200',NULL),
	(15,'/api/v0/hash/save','GET','{\"ec_address\":\"EC3SnieQ3DqNhC3s4W5q29Lyk4VNPGhhFQcAfPPcXZBHwegQpmmz\",\"file_hash\":\"0df11d7b495162fe8f26bec2202264d7594697d2937d9aa7cda2311f6f9bd54d\",\"file_size\":\"200\",\"file_name\":\"unittest\",\"save_remote\":\"0\"}','f_001','save file hash to cunchain network','test_default_normal','200',NULL),
	(6,'/api/v0/user/update','GET','{\"address\":None,\"avatar\":None,\"groups\":\"user\",\"name\":\"Tom\"}','f_001','update account information','test_default_normal','200',NULL),
	(23,'/api/v0/pay_token/create','GET','{\"amount\":\"0.1\"}','f_001','create qr code and address for token payment','test_default_normal','200',NULL),
	(19,'/api/v0/pay_wx/create','GET','{\"amount\":\"1\",\"product\":\"credit\"}','f_001','create a wechat pay order','test_default_normal','200',NULL),
	(21,'/api/v0/pay_wx/check','GET','{\"order_no\":None}','f_001','check state of wechat pay order','test_pay_wx_check','200',NULL),
	(18,'/api/v0/proof/list','GET','{\"start\":\"0\",\"count\":\"1\"}','f_001','get proof record list','test_default_normal','200',NULL),
	(20,'/api/v0/qr/image','GET','{\"uri\":None}','f_001','generate qr image','test_qr_image','200',NULL),
	(12,'/api/v0/transfer/credit','GET','{\"number\":\"000000000000000000\",\"amount\":\"10\",\"name\":\"Tom\",\"pass\":\"8969ffe739e4f97f7ad717e13eae75cfcb657e8d\"}','f_001','create a CREDIT transfer order','test_transfer','200',NULL),
	(13,'/api/v0/transfer/token','GET','{\"number\":\"000000000000000000\",\"amount\":\"10.1\",\"name\":\"超级管理员\",\"pass\":\"8969ffe739e4f97f7ad717e13eae75cfcb657e8d\"}','f_001','create a TOKEN transfer order','test_transfer','200',NULL),
	(7,'/api/v0/upload/img','POST','{\"img\":\"/tmp/1.png\"}','f_001','/api/v0/upload/img','test_upload_img','200',NULL),
	(8,'/api/v0/user/logout','GET','{}','f_001','user logout','test_default_normal','200',NULL),
	(3,'/api/v0/user/register','GET','{\'password\': \'8969ffe739e4f97f7ad717e13eae75cfcb657e8d\', \'name\': None, \'captcha_sms\': \'944466\', \'groups\': \'user\', \'phone_no\': \'137715096782\', \'account\': \'test_137715096782\'}','f_001','register new user account','test_register_normal','200',NULL),
	(1,'/api/v0/captcha/image','GET','{\"reason\":\"register\",\"test\":\"true\"}','f_001','get captcha image','test_default_normal','200',NULL),
	(4,'/api/v0/user/login','GET','{}','f_001','login','test_login_normal','200',NULL),
	(10,'/api/v0/org/user/info','GET','{\"number\":None}','f_001','get user status','test_org_user_info','200',NULL),
	(11,'/api/v0/org/user/update','POST','{}','f_001','update account information in my organization','test_org_user_update','200',NULL),
	(14,'/api/v0/org/user/finance/list','GET','{\"start\":0,\"count\":1,\"search\":0,\"date_from\":-1,\"date_to\":-1,\"orderby\":None,\"desc\":None,\"number\":\"000001000000000005\",\"type\":\"charge,transfer,consume\"}','f_001','get finance record list','test_org_user_finance','200',NULL),
	(25,'/api/v0/org/user/list','GET','{\"start\":0,\"count\":10,\"search\":,\"orderby\":None,\"desc\":0,\"groups\":\"user,org\",\"authenticated\":\"0,1\"}','f_001','list all users under organization','test_default_normal','200',NULL);

/*!40000 ALTER TABLE `usercase` ENABLE KEYS */;
UNLOCK TABLES;



--
-- Dumping routines (FUNCTION) for database 'unittest'
--
DELIMITER ;;

# Dump of FUNCTION currval
# ------------------------------------------------------------

/*!50003 DROP FUNCTION IF EXISTS `currval` */;;
/*!50003 SET SESSION SQL_MODE=""*/;;
/*!50003 CREATE*/ /*!50020 DEFINER=`root`@`%`*/ /*!50003 FUNCTION `currval`(seq_name VARCHAR(50)) RETURNS int(11)
    DETERMINISTIC
BEGIN
	DECLARE value INTEGER;
	SET value = 0;
	SELECT current_value INTO value
		FROM sequence
		WHERE name = seq_name;
	RETURN value;
END */;;

/*!50003 SET SESSION SQL_MODE=@OLD_SQL_MODE */;;
# Dump of FUNCTION nextval
# ------------------------------------------------------------

/*!50003 DROP FUNCTION IF EXISTS `nextval` */;;
/*!50003 SET SESSION SQL_MODE=""*/;;
/*!50003 CREATE*/ /*!50020 DEFINER=`root`@`%`*/ /*!50003 FUNCTION `nextval`(seq_name VARCHAR(50)) RETURNS int(11)
    DETERMINISTIC
BEGIN
	UPDATE sequence
		SET current_value = current_value + increment
		WHERE name = seq_name;
	RETURN currval(seq_name);
END */;;

/*!50003 SET SESSION SQL_MODE=@OLD_SQL_MODE */;;
# Dump of FUNCTION setval
# ------------------------------------------------------------

/*!50003 DROP FUNCTION IF EXISTS `setval` */;;
/*!50003 SET SESSION SQL_MODE=""*/;;
/*!50003 CREATE*/ /*!50020 DEFINER=`root`@`%`*/ /*!50003 FUNCTION `setval`(seq_name VARCHAR(50), value INTEGER) RETURNS int(11)
    DETERMINISTIC
BEGIN
	UPDATE sequence
		SET current_value = value
		WHERE name = seq_name;
	RETURN currval(seq_name);
END */;;

/*!50003 SET SESSION SQL_MODE=@OLD_SQL_MODE */;;
DELIMITER ;

/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
