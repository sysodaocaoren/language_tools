/*
 Navicat Premium Data Transfer

 Source Server         : localhost
 Source Server Type    : MySQL
 Source Server Version : 50725
 Source Host           : localhost:3306
 Source Schema         : news

 Target Server Type    : MySQL
 Target Server Version : 50725
 File Encoding         : 65001

 Date: 31/07/2024 22:01:56
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for t_comment_info
-- ----------------------------
DROP TABLE IF EXISTS `t_comment_info`;
CREATE TABLE `t_comment_info`  (
  `id` int(20) NOT NULL AUTO_INCREMENT,
  `content` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `news_id` int(20) NULL DEFAULT NULL,
  `user_id` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `user_name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `location_prov` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `create_time` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `location_city` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `view_point_tags` varchar(600) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `emo_tags` varchar(600) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `content_tags` varchar(600) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `zan_num` int(10) NULL DEFAULT NULL,
  `child_comment_num` int(10) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 7 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of t_comment_info
-- ----------------------------
INSERT INTO `t_comment_info` VALUES (2, '1', 1, '1', '1', '1', '1', '1', '1', '1', '1', 1, 1);
INSERT INTO `t_comment_info` VALUES (3, '1', 1, '1', '1', '1', '1', '1', '1', '1', '1', 1, 1);
INSERT INTO `t_comment_info` VALUES (4, '1', 1, '1', '1', '1', '1', '1', '1', '1', '1', 1, 1);
INSERT INTO `t_comment_info` VALUES (5, '1', 1, '1', '1', '1', '1', '1', '1', '1', '1', 1, 1);
INSERT INTO `t_comment_info` VALUES (6, '1', 1, '1', '1', '1', '1', '1', '1', '1', '1', 1, 1);

-- ----------------------------
-- Table structure for t_news_info
-- ----------------------------
DROP TABLE IF EXISTS `t_news_info`;
CREATE TABLE `t_news_info`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(800) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL DEFAULT NULL,
  `summry` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `user_id` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `create_time` varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `news_id` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `source_type` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 9 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of t_news_info
-- ----------------------------
INSERT INTO `t_news_info` VALUES (1, '1', '1', '1', '1', '1', '1');
INSERT INTO `t_news_info` VALUES (3, '1', '1', '1', '1', '1', '1');
INSERT INTO `t_news_info` VALUES (4, '1', '1', '1', '1', '1', '1');
INSERT INTO `t_news_info` VALUES (5, '1', '1', '1', '1', '1', '1');
INSERT INTO `t_news_info` VALUES (6, '1', '1', '1', '1', '1', '1');
INSERT INTO `t_news_info` VALUES (7, '1', '1', '1', '1', '1', '1');
INSERT INTO `t_news_info` VALUES (8, '1', '1', '1', '1', '1', '1');

-- ----------------------------
-- Table structure for t_serch_info
-- ----------------------------
DROP TABLE IF EXISTS `t_serch_info`;
CREATE TABLE `t_serch_info`  (
  `id` int(20) NOT NULL AUTO_INCREMENT,
  `keyword` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `news_id` int(20) NULL DEFAULT NULL,
  `create_time` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of t_serch_info
-- ----------------------------
INSERT INTO `t_serch_info` VALUES (1, '1', 1, '1');

SET FOREIGN_KEY_CHECKS = 1;
