CREATE TABLE `noc_sda` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `start_time` varchar(20) DEFAULT NULL,
  `manageIp` varchar(15) DEFAULT NULL,
  `bussIp` varchar(15) DEFAULT NULL,
  `linkNum` int(11) DEFAULT NULL,
  `linkStat` char(8) DEFAULT NULL,
  `linkAlm` varchar(30) DEFAULT NULL,
  `opc` char(8) DEFAULT NULL,
  `dpc` char(8) DEFAULT NULL,
  `slc` char(2) DEFAULT NULL,
  `msupck` varchar(255) DEFAULT NULL,
  `msubyte` varchar(255) DEFAULT NULL,
  `msudrop` varchar(255) DEFAULT NULL,
  `crcerr` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
