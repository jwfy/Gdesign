create table `user`(
    `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
    `name` varchar(20) NOT NULL default "",
    `email` varchar(30) NOT NULL default "",
    `password` varchar(200) NOT NULL default "",
    `login_time` datetime NOT NULL default "0000-00-00 00:00:00",
    `register_time` datetime NOT NULL default "0000-00-00 00:00:00",
    `status` int(5) NOT NULL default 0  comment '用户状态',
    `permission` int(5) NOT NULL default 0 comment '用户权限', 
    primary key(`id`),
    unique key `name`(`name`),
    unique key `email`(`email`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

