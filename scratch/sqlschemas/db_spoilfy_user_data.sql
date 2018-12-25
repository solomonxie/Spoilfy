# ************************************************************
# Sequel Pro SQL dump
# Version 4541
#
# http://www.sequelpro.com/
# https://github.com/sequelpro/sequelpro
#
# Host: 127.0.0.1 (MySQL 5.5.5-10.3.10-MariaDB)
# Database: db_spoilfy_user_lib
# Generation Time: 2018-12-10 09:37:38 +0000
# ************************************************************


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


# Dump of table fs_Playlists
# ------------------------------------------------------------

DROP TABLE IF EXISTS `fs_Playlists`;

CREATE TABLE `fs_Playlists` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `fs_ids` int(11) DEFAULT NULL,
  `tids` int(11) DEFAULT NULL,
  `path` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;



# Dump of table fs_Tracks
# ------------------------------------------------------------

DROP TABLE IF EXISTS `fs_Tracks`;

CREATE TABLE `fs_Tracks` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `tid` int(11) DEFAULT NULL,
  `path` text DEFAULT NULL,
  `file_info` text DEFAULT NULL,
  `tags` text DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;



# Dump of table hosts
# ------------------------------------------------------------

DROP TABLE IF EXISTS `hosts`;

CREATE TABLE `hosts` (
  `host_id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `host` text NOT NULL,
  `info` text DEFAULT NULL,
  `uri` text NOT NULL,
  `auth` longtext DEFAULT NULL,
  PRIMARY KEY (`host_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;



# Dump of table mp_Albums
# ------------------------------------------------------------

DROP TABLE IF EXISTS `mp_Albums`;

CREATE TABLE `mp_Albums` (
  `abid` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `spt_abid` int(11) DEFAULT NULL,
  `mb_abid` int(11) DEFAULT NULL,
  `itn_abid` int(11) DEFAULT NULL,
  PRIMARY KEY (`abid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;



# Dump of table mp_Tracks
# ------------------------------------------------------------

DROP TABLE IF EXISTS `mp_Tracks`;

CREATE TABLE `mp_Tracks` (
  `tid` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `spt_tid` int(11) DEFAULT NULL,
  `mb_tid` int(11) DEFAULT NULL,
  `itn_tid` int(11) DEFAULT NULL,
  `fs_ids` text DEFAULT NULL,
  PRIMARY KEY (`tid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;



# Dump of table u_Albums
# ------------------------------------------------------------

DROP TABLE IF EXISTS `u_Albums`;

CREATE TABLE `u_Albums` (
  `abid` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `uid` int(11) DEFAULT NULL,
  `title` int(11) DEFAULT NULL,
  `liked_date` int(11) DEFAULT NULL,
  `memo` int(11) DEFAULT NULL,
  PRIMARY KEY (`abid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;



# Dump of table u_Artists
# ------------------------------------------------------------

DROP TABLE IF EXISTS `u_Artists`;

CREATE TABLE `u_Artists` (
  `atid` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `uid` int(11) DEFAULT NULL,
  `name` int(11) DEFAULT NULL,
  `liked_date` int(11) DEFAULT NULL,
  `memo` int(11) DEFAULT NULL,
  PRIMARY KEY (`atid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;



# Dump of table u_Hosts
# ------------------------------------------------------------

DROP TABLE IF EXISTS `u_Hosts`;

CREATE TABLE `u_Hosts` (
  `huid` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `uid` int(11) unsigned NOT NULL,
  `host_id` int(11) unsigned NOT NULL DEFAULT 1,
  `auth` longtext DEFAULT NULL,
  `name` int(11) DEFAULT NULL,
  `nickname` int(11) DEFAULT NULL,
  `email` int(11) DEFAULT NULL,
  `info` int(11) DEFAULT NULL,
  PRIMARY KEY (`huid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;



# Dump of table u_Playlists
# ------------------------------------------------------------

DROP TABLE IF EXISTS `u_Playlists`;

CREATE TABLE `u_Playlists` (
  `plid` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `uid` int(11) unsigned NOT NULL,
  `title` varchar(100) NOT NULL DEFAULT '',
  `info` text DEFAULT NULL,
  `created_date` date DEFAULT NULL,
  `tids` text DEFAULT NULL,
  `memo` int(11) DEFAULT NULL,
  PRIMARY KEY (`plid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;



# Dump of table u_Recommends
# ------------------------------------------------------------

DROP TABLE IF EXISTS `u_Recommends`;

CREATE TABLE `u_Recommends` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `uid` int(11) NOT NULL,
  `title` int(11) NOT NULL,
  `info` int(11) NOT NULL,
  `abids` text DEFAULT NULL,
  `atids` text DEFAULT NULL,
  `plids` text DEFAULT NULL,
  `rcm_date` date DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;



# Dump of table u_Tracks
# ------------------------------------------------------------

DROP TABLE IF EXISTS `u_Tracks`;

CREATE TABLE `u_Tracks` (
  `tid` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `uid` int(11) unsigned NOT NULL,
  `name` varchar(11) NOT NULL DEFAULT '',
  `last_play` date DEFAULT NULL,
  `added_date` date DEFAULT NULL,
  `played_count` int(11) unsigned DEFAULT NULL,
  `rate` int(11) DEFAULT NULL,
  `memo` int(11) DEFAULT NULL,
  PRIMARY KEY (`tid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;



# Dump of table u_Users
# ------------------------------------------------------------

DROP TABLE IF EXISTS `u_Users`;

CREATE TABLE `u_Users` (
  `uid` int(11) NOT NULL,
  `uname` varchar(100) NOT NULL DEFAULT '',
  PRIMARY KEY (`uid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;




/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
