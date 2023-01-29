create database tmcit;
create table tmcit.userinfo(
    user_id int auto_increment,
    user_name varchar(10) not NULL,
    user_password varchar(50) unique not NULL,
    user_mailaddress varchar(50) not NULL,
    user_deletion int,
    date_registration date not NULL,
    date_lastlogin date not NULL,
    date_deletion date,
    PRIMARY KEY (user_id)
    );

create table tmcit.physicalinfo(
    id int auto_increment,
    user_id int,
    user_height float,
    user_weight float,
    user_age int,
    date_registration date,
    date_updated date,
    UNIQUE KEY (id),
    FOREIGN KEY(user_id) REFERENCES userinfo(user_id)
    );

create table tmcit.calorieinfo(
    id int auto_increment,
    user_id int,
    calorie_intake float,
    date_updated date,
    UNIQUE KEY (id),
    FOREIGN KEY(user_id) REFERENCES userinfo(user_id)
    );

create table tmcit.sleepinginfo(
    id int auto_increment,
    user_id int,
    sleeping_minutes int,
    date_updated date,
    UNIQUE KEY (id),
    FOREIGN KEY(user_id) REFERENCES userinfo(user_id)
    );

create table tmcit.fluidinfo(
    id int auto_increment,
    user_id int,
    fluid_intake float,
    date_updated date,
    UNIQUE KEY (id),
    FOREIGN KEY(user_id) REFERENCES userinfo(user_id)
    );


create table tmcit.execiseinfo(
    id int auto_increment,
    user_id int,
    execise_minutes int,
    execise_id varchar(5),
    date_updated date,
    PRIMARY KEY (execise_id),
    UNIQUE KEY (id),
    FOREIGN KEY(user_id) REFERENCES userinfo(user_id)
    );

create table tmcit.eventinfo(
    execise_id varchar(5),
    execise_event int,
    date_updated date,
    FOREIGN KEY(execise_id) REFERENCES execiseinfo(execise_id)
    );

