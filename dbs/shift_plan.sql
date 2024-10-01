-- --------------------------------------------------------
-- 主機:                           127.0.0.1
-- 伺服器版本:                        11.4.2-MariaDB - mariadb.org binary distribution
-- 伺服器作業系統:                      Win64
-- HeidiSQL 版本:                  12.6.0.6765
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- 傾印 shift_plan 的資料庫結構
CREATE DATABASE IF NOT EXISTS `shift_plan` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci */;
USE `shift_plan`;

-- 傾印  資料表 shift_plan.all_member_list 結構
CREATE TABLE IF NOT EXISTS `all_member_list` (
  `userNo` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `userName` varchar(50) NOT NULL,
  `userGrade` enum('Project_Manager','Regular_Member') DEFAULT 'Regular_Member',
  `userID` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL,
  PRIMARY KEY (`userNo`),
  UNIQUE KEY `userID` (`userID`),
  UNIQUE KEY `userName` (`userName`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci ROW_FORMAT=DYNAMIC COMMENT='管理使用者登入資訊';

-- 正在傾印表格  shift_plan.all_member_list 的資料：~5 rows (近似值)
DELETE FROM `all_member_list`;
INSERT INTO `all_member_list` (`userNo`, `userName`, `userGrade`, `userID`, `password`) VALUES
	(1, 'ADMIN', 'Project_Manager', 'admin', 'password'),
	(2, 'BEN', 'Regular_Member', 'ben', 'password'),
	(3, 'CARL', 'Regular_Member', 'carl', 'password'),
	(4, 'DON', 'Regular_Member', 'don', 'password'),
	(5, 'ELLE', 'Regular_Member', 'elle', 'password');

-- 傾印  資料表 shift_plan.all_project_list 結構
CREATE TABLE IF NOT EXISTS `all_project_list` (
  `projectID` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `projectName` varchar(50) NOT NULL,
  PRIMARY KEY (`projectID`),
  UNIQUE KEY `projectName` (`projectName`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='管理專案清單';

-- 正在傾印表格  shift_plan.all_project_list 的資料：~1 rows (近似值)
DELETE FROM `all_project_list`;
INSERT INTO `all_project_list` (`projectID`, `projectName`) VALUES
	(1, 'pro_test1');

-- 傾印  資料表 shift_plan.mem_pro_1 結構
CREATE TABLE IF NOT EXISTS `mem_pro_1` (
  `projectID` int(10) unsigned NOT NULL,
  `projectName` varchar(50) NOT NULL,
  PRIMARY KEY (`projectID`),
  CONSTRAINT `FK_member_project_admin_project_list` FOREIGN KEY (`projectID`) REFERENCES `all_project_list` (`projectID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci ROW_FORMAT=DYNAMIC COMMENT='\r\n';

-- 正在傾印表格  shift_plan.mem_pro_1 的資料：~1 rows (近似值)
DELETE FROM `mem_pro_1`;
INSERT INTO `mem_pro_1` (`projectID`, `projectName`) VALUES
	(1, 'pro_test1');

-- 傾印  資料表 shift_plan.mem_pro_2 結構
CREATE TABLE IF NOT EXISTS `mem_pro_2` (
  `projectID` int(10) unsigned NOT NULL,
  `projectName` varchar(50) NOT NULL,
  PRIMARY KEY (`projectID`) USING BTREE,
  CONSTRAINT `mem_pro_2_ibfk_1` FOREIGN KEY (`projectID`) REFERENCES `all_project_list` (`projectID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci ROW_FORMAT=DYNAMIC COMMENT='\r\n';

-- 正在傾印表格  shift_plan.mem_pro_2 的資料：~1 rows (近似值)
DELETE FROM `mem_pro_2`;
INSERT INTO `mem_pro_2` (`projectID`, `projectName`) VALUES
	(1, 'pro_test1');

-- 傾印  資料表 shift_plan.mem_pro_3 結構
CREATE TABLE IF NOT EXISTS `mem_pro_3` (
  `projectID` int(10) unsigned NOT NULL,
  `projectName` varchar(50) NOT NULL,
  PRIMARY KEY (`projectID`) USING BTREE,
  CONSTRAINT `mem_pro_3_ibfk_1` FOREIGN KEY (`projectID`) REFERENCES `all_project_list` (`projectID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci ROW_FORMAT=DYNAMIC COMMENT='\r\n';

-- 正在傾印表格  shift_plan.mem_pro_3 的資料：~1 rows (近似值)
DELETE FROM `mem_pro_3`;
INSERT INTO `mem_pro_3` (`projectID`, `projectName`) VALUES
	(1, 'pro_test1');

-- 傾印  資料表 shift_plan.mem_pro_4 結構
CREATE TABLE IF NOT EXISTS `mem_pro_4` (
  `projectID` int(10) unsigned NOT NULL,
  `projectName` varchar(50) NOT NULL,
  PRIMARY KEY (`projectID`) USING BTREE,
  CONSTRAINT `mem_pro_4_ibfk_1` FOREIGN KEY (`projectID`) REFERENCES `all_project_list` (`projectID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci ROW_FORMAT=DYNAMIC COMMENT='\r\n';

-- 正在傾印表格  shift_plan.mem_pro_4 的資料：~1 rows (近似值)
DELETE FROM `mem_pro_4`;
INSERT INTO `mem_pro_4` (`projectID`, `projectName`) VALUES
	(1, 'pro_test1');

-- 傾印  資料表 shift_plan.mem_pro_5 結構
CREATE TABLE IF NOT EXISTS `mem_pro_5` (
  `projectID` int(10) unsigned NOT NULL,
  `projectName` varchar(50) NOT NULL,
  PRIMARY KEY (`projectID`) USING BTREE,
  CONSTRAINT `mem_pro_5_ibfk_1` FOREIGN KEY (`projectID`) REFERENCES `all_project_list` (`projectID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci ROW_FORMAT=DYNAMIC COMMENT='\r\n';

-- 正在傾印表格  shift_plan.mem_pro_5 的資料：~1 rows (近似值)
DELETE FROM `mem_pro_5`;
INSERT INTO `mem_pro_5` (`projectID`, `projectName`) VALUES
	(1, 'pro_test1');

-- 傾印  資料表 shift_plan.mem_unavai_1 結構
CREATE TABLE IF NOT EXISTS `mem_unavai_1` (
  `unavailableDays` date NOT NULL,
  UNIQUE KEY `unavailableDays` (`unavailableDays`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- 正在傾印表格  shift_plan.mem_unavai_1 的資料：~16 rows (近似值)
DELETE FROM `mem_unavai_1`;
INSERT INTO `mem_unavai_1` (`unavailableDays`) VALUES
	('2024-09-02'),
	('2024-09-04'),
	('2024-09-08'),
	('2024-09-09'),
	('2024-09-10'),
	('2024-09-11'),
	('2024-09-12'),
	('2024-09-14'),
	('2024-09-17'),
	('2024-09-18'),
	('2024-09-19'),
	('2024-09-21'),
	('2024-09-22'),
	('2024-09-24'),
	('2024-09-25'),
	('2024-09-27');

-- 傾印  資料表 shift_plan.mem_unavai_2 結構
CREATE TABLE IF NOT EXISTS `mem_unavai_2` (
  `unavailableDays` date NOT NULL,
  UNIQUE KEY `unavailableDays` (`unavailableDays`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci ROW_FORMAT=DYNAMIC;

-- 正在傾印表格  shift_plan.mem_unavai_2 的資料：~6 rows (近似值)
DELETE FROM `mem_unavai_2`;
INSERT INTO `mem_unavai_2` (`unavailableDays`) VALUES
	('2024-09-10'),
	('2024-09-11'),
	('2024-09-17'),
	('2024-09-18'),
	('2024-09-24'),
	('2024-09-25');

-- 傾印  資料表 shift_plan.mem_unavai_3 結構
CREATE TABLE IF NOT EXISTS `mem_unavai_3` (
  `unavailableDays` date NOT NULL,
  UNIQUE KEY `unavailableDays` (`unavailableDays`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci ROW_FORMAT=DYNAMIC;

-- 正在傾印表格  shift_plan.mem_unavai_3 的資料：~4 rows (近似值)
DELETE FROM `mem_unavai_3`;
INSERT INTO `mem_unavai_3` (`unavailableDays`) VALUES
	('2024-09-04'),
	('2024-09-11'),
	('2024-09-18'),
	('2024-09-25');

-- 傾印  資料表 shift_plan.mem_unavai_4 結構
CREATE TABLE IF NOT EXISTS `mem_unavai_4` (
  `unavailableDays` date NOT NULL,
  UNIQUE KEY `unavailableDays` (`unavailableDays`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci ROW_FORMAT=DYNAMIC;

-- 正在傾印表格  shift_plan.mem_unavai_4 的資料：~4 rows (近似值)
DELETE FROM `mem_unavai_4`;
INSERT INTO `mem_unavai_4` (`unavailableDays`) VALUES
	('2024-09-05'),
	('2024-09-12'),
	('2024-09-19'),
	('2024-09-26');

-- 傾印  資料表 shift_plan.mem_unavai_5 結構
CREATE TABLE IF NOT EXISTS `mem_unavai_5` (
  `unavailableDays` date NOT NULL,
  UNIQUE KEY `unavailableDays` (`unavailableDays`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci ROW_FORMAT=DYNAMIC;

-- 正在傾印表格  shift_plan.mem_unavai_5 的資料：~4 rows (近似值)
DELETE FROM `mem_unavai_5`;
INSERT INTO `mem_unavai_5` (`unavailableDays`) VALUES
	('2024-09-06'),
	('2024-09-13'),
	('2024-09-20'),
	('2024-09-27');

-- 傾印  資料表 shift_plan.pro_test1 結構
CREATE TABLE IF NOT EXISTS `pro_test1` (
  `userNo` int(11) unsigned NOT NULL,
  `userName` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`userNo`) USING BTREE,
  UNIQUE KEY `userName` (`userName`),
  CONSTRAINT `FK_project_test1_member_list` FOREIGN KEY (`userNo`) REFERENCES `all_member_list` (`userNo`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- 正在傾印表格  shift_plan.pro_test1 的資料：~5 rows (近似值)
DELETE FROM `pro_test1`;
INSERT INTO `pro_test1` (`userNo`, `userName`) VALUES
	(1, 'ADMIN'),
	(2, 'BEN'),
	(3, 'CARL'),
	(4, 'DON'),
	(5, 'ELLE');

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
