create table `comment`(
    `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
    `name` varchar(20) NOT NULL ,
    `email` varchar(30) NOT NULL,
    `title` varchar(30) NOT NULL comment "评论的标题",
    `contain` varchar(140) NOT NULL comment "评论的内容",
    `category` varchar(10) NOT NULL default "movie" comment "评论的类目",
    `time` datetime NOT NULL,
    `status` int(5) NOT NULL comment '评论状态，可以隐藏，显示',
    `ip` varchar(20) NOT NULL default "127.0.0.1" comment "发表评论的ip地址",
    `_id` varchar(30) NOT NULL default "" comment "mongo 数据库 id字段",
    primary key(`id`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

