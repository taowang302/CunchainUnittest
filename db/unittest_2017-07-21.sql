# ************************************************************
# Sequel Pro SQL dump
# Version 4541
#
# http://www.sequelpro.com/
# https://github.com/sequelpro/sequelpro
#
# Host: 192.168.168.137 (MySQL 5.6.19)
# Database: unittest
# Generation Time: 2017-07-21 06:11:41 +0000
# ************************************************************


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


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
	('f_001','192.168.10.171',8888,'/api/v0','test',NULL);

/*!40000 ALTER TABLE `file_bag` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table test_result
# ------------------------------------------------------------

DROP TABLE IF EXISTS `test_result`;

CREATE TABLE `test_result` (
  `from_view_id` varchar(32) NOT NULL COMMENT '用例归档编号',
  `case_number` varchar(32) NOT NULL COMMENT '用例编号',
  `except_response_code` varchar(32) NOT NULL COMMENT '预期返回确认码',
  `except_response` varchar(1000) DEFAULT '' COMMENT '预期返回结果',
  `actual_response_code` varchar(32) DEFAULT NULL COMMENT '实际返回确认码',
  `actual_response` varchar(1000) DEFAULT NULL COMMENT '实际返回结果',
  `result` varchar(128) DEFAULT NULL COMMENT '用例执行结果',
  `description` varchar(1000) DEFAULT NULL COMMENT '执行结果说明'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `test_result` WRITE;
/*!40000 ALTER TABLE `test_result` DISABLE KEYS */;

INSERT INTO `test_result` (`from_view_id`, `case_number`, `except_response_code`, `except_response`, `actual_response_code`, `actual_response`, `result`, `description`)
VALUES
	('f_001','1','200','{\"result\": \"success\"}','200','{\"result\": \"success\"}','Pass',NULL),
	('f_001','2','200','','200','{\"user\": {\"id_card_image_1\": \"23b97e4e-74cf-4502-a974-ea635809ed7c.png\", \"id_card_image_2\": \"bd1d0e0d-5379-4779-8eb5-2b4e168ae260.png\", \"phone_no2\": \"None\", \"avatar\": \"None\", \"token\": 99, \"email2\": \"None\", \"address\": \"None\", \"id_card\": null, \"name\": \"wangt\", \"org_number\": \"000000000000000000\", \"authenticated\": 1, \"credit_cny_rate\": 1, \"email\": \"None\", \"groups\": \"user\", \"id_card_image_0\": \"b13ed4b7-5af4-451b-8e0f-3666aca68cbe\", \"account\": \"wangt\", \"phone_no\": \"18142003340\", \"register_time\": \"2017-07-05T02:02:04.000Z\", \"number\": \"000001000000000002\", \"credit\": 100}, \"result\": \"success\"}','Pass',NULL),
	('f_001','3','200','','200','{\"start\": 0, \"count\": 1, \"total\": 3, \"result\": \"success\", \"data_list\": [{\"origin_number\": \"000001000000000002\", \"origin_credit\": 100, \"amount\": 100, \"remark\": null, \"state\": \"SUCCESS\", \"time_start\": \"2017-07-20T03:41:14.000Z\", \"origin_token\": 0, \"transfer_number\": 62, \"type\": \"TRANSFER\", \"target_number\": \"000000000000000000\", \"time_end\": \"2017-07-20T03:41:14.000Z\", \"currency\": \"TOKEN\"}]}','Pass',NULL),
	('f_001','4','200','','200','{\"result\": \"not implement yet\"}','Fail',NULL),
	('f_001','5','200','{\"result\": \"success\"}','200','{\"entry_status\": {\"text\": \"{\"hash\":\"231797977e8f94e40a4e04a2c9b6b67722d3b394bdd16b2800749fb97af1362e\",\"time\":\"2017-07-20T08:25:31.908Z\",\"size\":12836,\"name\":\"1.png\",\"save_remote\":0}\", \"chainid\": \"20c305d6fd1a0e01b9d560580aa10bff84b59e211cfdc3861ce66015391dd886\", \"extids\": [\"231797977e8f94e40a4e04a2c9b6b67722d3b394bdd16b2800749fb97af1362e\"]}, \"result\": \"success\"}','Pass',NULL),
	('f_001','6','200','','200','{\"result\": \"name uncorrect\"}','Fail',NULL),
	('f_001','7','200','','200','{\"chain_host\": \"\", \"offset\": 0, \"files\": [{\"entry_hash\": \"EC3SnieQ3DqNhC3s4W5q29Lyk4VNPGhhFQcAfPPcXZBHwegQpmmz\", \"file\": null}, {\"entry_hash\": \"21a8aa5e52d1dfd640f48e36f6dccd64c32f3f6957f68e05f3eeea94e32cf1bb\", \"file\": {\"name\": \"unittest\", \"time\": \"2017-07-21T02:21:10.636Z\", \"hash\": \"0df11d7b495162fe8f26bec2202264d7594697d2937d9aa7cda2311f6f9bd54d\", \"save_remote\": 0, \"size\": \"200\"}}], \"count\": 16, \"result\": \"success\", \"limit\": 1}','Pass',NULL),
	('f_001','8','200','','200','{\"chain_host\": \"\", \"result\": \"success\", \"entry_hash\": \"66b03c984efcdd62841ee85d2d0939a993e8daeb2998fc85c1b4755079d7ce62\"}','Pass',NULL),
	('f_001','9','200','','200','{\"result\": \"email exists\"}','Fail',NULL),
	('f_001','10','200','','200','{\"result\": \"not implement yet\"}','Fail',NULL),
	('f_001','11','200','','200','{\"order_no\": \"0000000000000147\", \"result\": \"success\", \"pay_uri\": \"weixin://wxpay/bizpayurl?pr=TSj4TBJ\"}','Pass',NULL),
	('f_001','12','200','','200','{\"sale_state\": \"not_sell\", \"result\": \"success\", \"pay_state\": \"checking\"}','Pass',NULL),
	('f_001','13','200','','200','{\"start\": 0, \"count\": 1, \"total\": 23, \"result\": \"success\", \"data_list\": [{\"time\": \"2017-07-21T05:35:43.000Z\", \"account_number\": \"000001000000000002\", \"file_name\": \"unittest\", \"save_remote\": 0, \"file_size\": 200, \"entry_hash\": \"66b03c984efcdd62841ee85d2d0939a993e8daeb2998fc85c1b4755079d7ce62\", \"file_hash\": \"0df11d7b495162fe8f26bec2202264d7594697d2937d9aa7cda2311f6f9bd54d\"}]}','Pass',NULL),
	('f_001','14','200','','200','{}','Pass',NULL),
	('f_001','15','200','','200','{\"result\": \"name uncorrect\"}','Fail',NULL),
	('f_001','16','200','','200','{\"result\": \"name uncorrect\"}','Fail',NULL),
	('f_001','17','200','','200','{\'url\': \'2e86b32c-194d-4b30-95eb-0a9b3bb01734\', \'result\': \'success\'}','Pass',NULL),
	('f_001','18','200','','200','{\"result\": \"success\"}','Pass',NULL),
	('f_001','19','200','','200','{\"param\": \"/api/v0/user/register?account=<account>&password=<password>&groups=<user|org>&captcha_sms=<captcha_sms>&[name=<name>]&[phone_no=<phone_no>]&[phone_no2=<phone_no2>]&[email=<email>]&[email2=<email2>]&[address=<address>]&[avatar=<avatar>]&[org_number=<org_number>]&[contact_name=<contact_name>]\", \"description\": \"register new user account\", \"result\": \"help\", \"return\": [\"{\"result\": <error_string>}\", \"{\"result\": \"success\"}\"]}','Fail',NULL);

/*!40000 ALTER TABLE `test_result` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table usercase
# ------------------------------------------------------------

DROP TABLE IF EXISTS `usercase`;

CREATE TABLE `usercase` (
  `case_number` varchar(32) NOT NULL COMMENT '用例编号',
  `case_name` varchar(128) NOT NULL COMMENT '用例名称',
  `http_method` varchar(5) NOT NULL COMMENT '交互方式',
  `queryparameters` varchar(1000) NOT NULL COMMENT '接口所需参数',
  `from_view_id` varchar(32) NOT NULL COMMENT '用例归属档案编号',
  `description` varchar(128) DEFAULT NULL COMMENT '用例说明',
  `test_method` varchar(32) DEFAULT NULL COMMENT '测试方法'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `usercase` WRITE;
/*!40000 ALTER TABLE `usercase` DISABLE KEYS */;

INSERT INTO `usercase` (`case_number`, `case_name`, `http_method`, `queryparameters`, `from_view_id`, `description`, `test_method`)
VALUES
	('1','/api/v0/user/login','GET','{\"user\":\"wangt\",\"password\":\"8969ffe739e4f97f7ad717e13eae75cfcb657e8d\"}','f_001','login','test_default_normal'),
	('2','/api/v0/user/info','GET','{}','f_001','info','test_default_normal'),
	('3','/api/v0/finance/list','GET','{\"start\":0,\"count\":1,\"search\":None,\"date_from\":-1,\"date_to\":-1,\"orderby\":None,\"desc\":0,\"number\":None,\"type\":None}','f_001','info','test_default_normal'),
	('4','/api/v0/pay_token/create','GET','{\"amount\":1}','f_001',NULL,'test_default_normal'),
	('5','/api/v0/status/entry','GET','{\"entry_hash\":\"a145e4c7f8b8f85c5d110b1fbe96cfb4c4237f7cb31cc4b653dc2c872d2cb67d\"}','f_001','get entry info','test_default_normal'),
	('6','/api/v0/transfer/token','POST','{\"amount\":\"1\",\"name\":\"wangt\",\"number\":\"000000000000000000\",\"pass\":\"8969ffe739e4f97f7ad717e13eae75cfcb657e8d\"}','f_001','transfer token','test_default_normal'),
	('7','/api/v0/hash/load','GET','{\"limit\":1,\"file_hash\":\"0df11d7b495162fe8f26bec2202264d7594697d2937d9aa7cda2311f6f9bd54d\",\"entry_hash\":\"EC3SnieQ3DqNhC3s4W5q29Lyk4VNPGhhFQcAfPPcXZBHwegQpmmz\"}','f_001','load hash','test_default_normal'),
	('8','/api/v0/hash/save','GET','{\"ec_address\":\"EC3SnieQ3DqNhC3s4W5q29Lyk4VNPGhhFQcAfPPcXZBHwegQpmmz\",\"file_hash\":\"0df11d7b495162fe8f26bec2202264d7594697d2937d9aa7cda2311f6f9bd54d\",\"file_size\":\"200\",\"file_name\":\"unittest\",\"save_remote\":\"0\"}','f_001','save hash','test_default_normal'),
	('9','/api/v0/user/update','GET','{\"account\":\"wangt\",\"address\":None,\"authenticated\":1,\"avatar\":None,\"email\":None,\"email2\":None,\"groups\":\"user\",\"name\":\"wangt\",\"number\":\"000001000000000002\",\"org_number\":\"000001000000000000\",\"password\":\"8969ffe739e4f97f7ad717e13eae75cfcb657e8d\",\"phone_no\":\"18142003340\",\"phone_no2\":None,\"register_time\":\"2017-07-05T02:02:04.000Z\"}','f_001','update account information','test_default_normal'),
	('10','/api/v0/pay_token/create','GET','{\"amount\":\"0.01\"}','f_001','create qr code and address for token payment','test_default_normal'),
	('11','/api/v0/pay_wx/create','GET','{\"amount\":\"1\",\"product\":\"credit\"}','f_001',NULL,'test_default_normal'),
	('12','/api/v0/pay_wx/check','GET','{\"order_no\":None}','f_001',NULL,'test_pay_wx_check'),
	('13','/api/v0/proof/list','GET','{\"start\":\"0\",\"count\":\"1\"}','f_001',NULL,'test_default_normal'),
	('14','/api/v0/qr/image','GET','{\"uri\":None}','f_001',NULL,'test_qr_image'),
	('15','/api/v0/transfer/credit','GET','{\"number\":\"000000000000000000\",\"amount\":\"1\",\"name\":\"wangt\",\"pass\":\"8969ffe739e4f97f7ad717e13eae75cfcb657e8d\"}','f_001',NULL,'test_default_normal'),
	('16','/api/v0/transfer/token','GET','{\"number\":\"000000000000000000\",\"amount\":\"100\",\"name\":\"wangt\",\"pass\":\"8969ffe739e4f97f7ad717e13eae75cfcb657e8d\"}','f_001',NULL,'test_default_normal'),
	('17','/api/v0/upload/img','POST','{\"img\":\"/tmp/1.png\"}','f_001',NULL,'test_upload_img'),
	('18','/api/v0/user/logout','GET','{}','f_001','user logout','test_default_normal'),
	('19','/api/v0/user/register','GET','{\"account\":\"jbitest\",\"address\":None,\"authenticated\":1,\"avatar\":None,\"email\":None,\"email2\":None,\"groups\":\"user\",\"name\":\"jbitest\",\"number\":\"000001000000000002\",\"org_number\":\"000001000000000000\",\"password\":\"8969ffe739e4f97f7ad717e13eae75cfcb657e8d\",\"phone_no\":\"18242003340\",\"phone_no2\":None}','f_001','register new user account','test_default_normal');

/*!40000 ALTER TABLE `usercase` ENABLE KEYS */;
UNLOCK TABLES;



/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
