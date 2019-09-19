/*
 Navicat MySQL Data Transfer

 Source Server         : ElvisCT
 Source Server Type    : MySQL
 Source Server Version : 80016
 Source Host           : localhost:3306
 Source Schema         : bokeyuan

 Target Server Type    : MySQL
 Target Server Version : 80016
 File Encoding         : 65001

 Date: 19/09/2019 09:54:57
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for articleinfo
-- ----------------------------
DROP TABLE IF EXISTS `articleinfo`;
CREATE TABLE `articleinfo`  (
  `author` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '作者',
  `issue_time` datetime(0) NULL DEFAULT NULL COMMENT '发布时间',
  `num_comment` int(10) NULL DEFAULT NULL COMMENT '评论数',
  `num_read` int(10) NULL DEFAULT NULL COMMENT '阅读数',
  `title` varchar(480) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '标题',
  `num_recommend` int(10) NULL DEFAULT NULL COMMENT '推荐数',
  PRIMARY KEY (`author`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of articleinfo
-- ----------------------------
INSERT INTO `articleinfo` VALUES ('Android阿沁', '2019-09-17 18:41:00', 0, 154, 'App 冷启动与热启动及启动白屏优化', 0);
INSERT INTO `articleinfo` VALUES ('baby_duoduo', '2019-09-17 21:18:00', 0, 153, '深入理解three.js中光源', 0);
INSERT INTO `articleinfo` VALUES ('basasuya', '2019-09-17 16:40:00', 0, 156, 'linux非root用户下安装软件，搭建生产环境', 0);
INSERT INTO `articleinfo` VALUES ('feiyun0112', '2019-09-17 21:13:00', 0, 127, 'ML.NET 示例：手写数字识别', 1);
INSERT INTO `articleinfo` VALUES ('gaoyanliang', '2019-09-17 19:45:00', 0, 108, 'kafka 主题管理', 0);
INSERT INTO `articleinfo` VALUES ('GrimMjx', '2019-09-17 21:07:00', 0, 103, 'Kafka源码分析及图解原理之Broker端', 0);
INSERT INTO `articleinfo` VALUES ('JadePeng', '2019-09-17 20:01:00', 0, 112, '教程 —— 如何在自己的应用集成superset', 0);
INSERT INTO `articleinfo` VALUES ('Kevin_zheng', '2019-09-17 15:23:00', 0, 287, 'zookeeper学习(一)_简介', 0);
INSERT INTO `articleinfo` VALUES ('东北小狐狸', '2019-09-17 19:30:00', 0, 88, '安装Harbor管理镜像服务', 1);
INSERT INTO `articleinfo` VALUES ('冰乐', '2019-09-17 21:14:00', 1, 304, '一次百度前端在线笔试题的经历与反思', 0);
INSERT INTO `articleinfo` VALUES ('冰封一夏', '2019-09-17 15:23:00', 4, 1082, '（六十七）c#Winform自定义控件-柱状图', 25);
INSERT INTO `articleinfo` VALUES ('咸鱼也要有梦想', '2019-09-17 16:51:00', 2, 173, '(一)ArrayList集合源码解析', 2);
INSERT INTO `articleinfo` VALUES ('布禾卡斐先生', '2019-09-17 18:28:00', 0, 106, 'SpringCloud学习笔记(4)：Hystrix容错机制', 0);
INSERT INTO `articleinfo` VALUES ('张善友', '2019-09-17 20:30:00', 4, 675, '微软发布.Net Core 3.0 RC1，最终版本定于9月23日', 10);
INSERT INTO `articleinfo` VALUES ('树杈', '2019-09-17 20:27:00', 0, 153, 'ASP.NET Core SignalR：集线器Hubs', 2);
INSERT INTO `articleinfo` VALUES ('猫咪大王_lkb', '2019-09-17 19:17:00', 0, 98, '自定义注解实战', 1);
INSERT INTO `articleinfo` VALUES ('神牛003', '2019-09-17 17:24:00', 0, 247, 'springboot数据库主从方案', 1);
INSERT INTO `articleinfo` VALUES ('美团技术团队', '2019-09-17 18:09:00', 0, 226, '美团集群调度系统HULK技术演进', 3);
INSERT INTO `articleinfo` VALUES ('腾讯云开发TCB', '2019-09-17 15:14:00', 0, 141, '云开发的数据库权限机制解读丨云开发101', 0);
INSERT INTO `articleinfo` VALUES ('闻人的技术博客', '2019-09-17 19:42:00', 1, 133, 'Java单元测试之JUnit 5快速上手', 0);

SET FOREIGN_KEY_CHECKS = 1;
