create table pachong.article
(
    id int(4) auto_increment comment '主键'
        primary key,
    company varchar(32) null comment '公司',
    title varchar(128) null comment '文章标题',
    href varchar(255) null comment '引用?',
    source varchar(255) null comment '来源',
    date varchar(255) null comment '文章日期',
    create_time datetime null on update CURRENT_TIMESTAMP comment '创建日期',
    score bigint null comment '分数'
);

