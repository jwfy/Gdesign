create table `user`(
    `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
    `name` varchar(20) NOT NULL,
    `email` varchar(30) NOT NULL,
    `password` varchar(200) NOT NULL,
    `login_time` datetime NOT NULL,
    `register_time` datetime NOT NULL,
    `status` int(5) NOT NULL default 0  comment '用户状态',
    `permission` int(5) NOT NULL default 0 comment '用户权限', 
    primary key(`id`),
    unique key `name`(`name`),
    unique key `email`(`email`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

