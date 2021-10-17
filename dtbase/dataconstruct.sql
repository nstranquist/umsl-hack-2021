DROP TABLE IF EXISTS `model`;
CREATE TABLE IF NOT EXISTS `model` (
  `id` int(2) NOT NULL,
  `name` varchar(40) NOT NULL,
  `vote` int(11) NOT NULL
)ENGINE=InnoDB DEFAULT CHARSET=latin1;

INSERT INTO `model`(`id`,`name`,`vote`) VALUES
(0,'Bert',0),
(1,'Term Frequency — Inverse Document Frequency',0);

CREATE TABLE IF NOT EXISTS `pastresearch` (
  `id` int(5) NOT NULL,
  `url` varchar(50),
  `header` varchar(50),
  `body` varchar(1000),
  `score` varchar(100) NOT NULL
)ENGINE=InnoDB DEFAULT CHARSET=latin1;

