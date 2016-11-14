


create database web_db;
create table if not exists ssserver(
    port int NOT NULL  key,
    password char(20) NOT NULL,
    type tinyint default 0 comment " 0 public 1 login 2 donate",
    owner char(50),
    state tinyint, 
    used int default 0,
    last_update timestamp,
    create_time datetime
    )engine=innodb;

create table if not exists user(
    user char(30) key,
    password char(64)  comment "default is null",
    used_flow float default 0 comment "MB",
    total_flow int default 0 comment "MB",
    type tinyint default 1 comment " 0 public 1 login 2 donate",
    donate_money float default 0,
    create_time datetime
    )engine=innodb;

