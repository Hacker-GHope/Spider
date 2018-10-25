'创建数据库'
create database jdSeacrh;
'创建数据表表'
create table seacrh_gufeng(id int auto_increment not null primary key,sku varchar(128),title varchar(128),price varchar(64),
shop varchar(128),commit varchar(128),img varchar(256),link varchar(256))engine=innodb charset=utf8;