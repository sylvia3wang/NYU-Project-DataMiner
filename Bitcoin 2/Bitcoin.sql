/*
Navicat MySQL Data Transfer

Source Server         : localhost
Source Server Version : 50529
Source Host           : localhost:3306
Source Database       : bitcoin

Target Server Type    : MYSQL
Target Server Version : 50529
File Encoding         : 65001

Date: 2018-12-12 23:29:13
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for pl
-- ----------------------------
DROP TABLE IF EXISTS `pl`;
CREATE TABLE `pl` (
  `PL_ID` int(11) NOT NULL AUTO_INCREMENT,
  `PL_balance` float(11,0) DEFAULT NULL,
  `VWAP` float(11,0) DEFAULT NULL,
  `UPL` float(11,0) DEFAULT NULL,
  `RPL` float(11,0) DEFAULT NULL,
  `symbol_symbol_ID` int(11) NOT NULL,
  `trade_id` bigint(20) NOT NULL,
  `total_assets` float DEFAULT NULL,
  PRIMARY KEY (`PL_ID`),
  KEY `symbol_ID_idx` (`symbol_symbol_ID`),
  KEY `trade_ID` (`trade_id`),
  CONSTRAINT `symbol_ID` FOREIGN KEY (`symbol_symbol_ID`) REFERENCES `symbol` (`symbol_ID`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `trade_ID` FOREIGN KEY (`trade_id`) REFERENCES `trade` (`trade_ID`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=1008 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of pl
-- ----------------------------
INSERT INTO `pl` VALUES ('1001', '500000', '0', '0', '0', '1', '1', '500000');
INSERT INTO `pl` VALUES ('1002', '496584', '3416', '0', '0', '1', '2', '500000');
INSERT INTO `pl` VALUES ('1003', '489736', '3421', '3', '3', '1', '3', '500008');
INSERT INTO `pl` VALUES ('1004', '496586', '3423', '7', '0', '1', '4', '500011');
INSERT INTO `pl` VALUES ('1005', '493169', '3420', '-3', '-3', '1', '5', '500003');
INSERT INTO `pl` VALUES ('1006', '489751', '3419', '-3', '-3', '1', '6', '500005');
INSERT INTO `pl` VALUES ('1007', '493169', '3419', '-2', '0', '1', '7', '500006');

-- ----------------------------
-- Table structure for side
-- ----------------------------
DROP TABLE IF EXISTS `side`;
CREATE TABLE `side` (
  `side_index` int(11) NOT NULL,
  `side_type` varchar(1) DEFAULT NULL,
  PRIMARY KEY (`side_index`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of side
-- ----------------------------
INSERT INTO `side` VALUES ('-1', 'B');
INSERT INTO `side` VALUES ('1', 'S');

-- ----------------------------
-- Table structure for symbol
-- ----------------------------
DROP TABLE IF EXISTS `symbol`;
CREATE TABLE `symbol` (
  `symbol_ID` int(11) NOT NULL,
  `symbol_name` varchar(55) DEFAULT NULL,
  PRIMARY KEY (`symbol_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of symbol
-- ----------------------------
INSERT INTO `symbol` VALUES ('1', 'BTC');

-- ----------------------------
-- Table structure for trade
-- ----------------------------
DROP TABLE IF EXISTS `trade`;
CREATE TABLE `trade` (
  `trade_ID` bigint(11) NOT NULL,
  `trade_qty` float DEFAULT NULL,
  `price` float DEFAULT NULL,
  `time` datetime DEFAULT NULL,
  `total_qty` float DEFAULT NULL,
  `cash` float DEFAULT NULL,
  `side_side_index` int(11) NOT NULL,
  `symbol_symbol_ID` int(11) NOT NULL,
  PRIMARY KEY (`trade_ID`),
  KEY `fk_trade_side1_idx` (`side_side_index`),
  KEY `fk_trade_symbol1_idx` (`symbol_symbol_ID`),
  CONSTRAINT `fk_trade_side1` FOREIGN KEY (`side_side_index`) REFERENCES `side` (`side_index`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_trade_symbol1` FOREIGN KEY (`symbol_symbol_ID`) REFERENCES `symbol` (`symbol_ID`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of trade
-- ----------------------------
INSERT INTO `trade` VALUES ('1', '0', '0', '1971-01-01 00:00:00', '0', '0', '-1', '1');
INSERT INTO `trade` VALUES ('2', '1', '3415.87', '2018-12-12 21:27:39', '1', '3415.87', '-1', '1');
INSERT INTO `trade` VALUES ('3', '2', '3424.18', '2018-12-12 21:51:49', '3', '6848.36', '-1', '1');
INSERT INTO `trade` VALUES ('4', '2', '3425.04', '2018-12-12 21:55:55', '1', '6850.08', '1', '1');
INSERT INTO `trade` VALUES ('5', '1', '3417.26', '2018-12-12 21:58:49', '2', '3417.26', '-1', '1');
INSERT INTO `trade` VALUES ('6', '1', '3418', '2018-12-12 22:00:03', '3', '3418', '-1', '1');
INSERT INTO `trade` VALUES ('7', '1', '3418.26', '2018-12-12 22:01:08', '2', '3418.26', '1', '1');
