create table `movie_recomment`(
    `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
    `title` char(20) NOT NULL comment "电影标题",
    `time` datetime NOT NULL comment "推荐的时间",
    `update_time` datetime NOT NULL comment "更新的时间",
    `status` int(5) NOT NULL comment '状态，只可以上线和下线，一旦添加不可修改',
    `_id` varchar(30) NOT NULL default "" comment "mongo 数据库 _id字段",
    `img_url` varchar(200) NOT NULL comment "推荐的电影大图图片",
    primary key(`id`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

