create database innovation;
use innovation;
drop database innovation;

create table user(
uID int not null auto_increment,
fname varchar(50) not null,
lname varchar(50) not null,
gender varchar(10) ,
phone varchar(20) not null,
email varchar(50) not null,
passwrd varchar(30) not null,
department varchar(50) not null,
isadmin int not null default 0,
constraint user_pk primary key(uID));

alter table user add constraint email_uniqe unique(email);



create table category(
cID int not null auto_increment,
cateogry_name varchar(20),
constraint category_pk primary key(cID));


create table idea(
iID int not null auto_increment,
uID int not null,
idea_desc varchar(200) not null,
cID int not null,
title varchar(20) not null unique,
status varchar(20) not null default 'initiated',
created datetime not null DEFAULT CURRENT_TIMESTAMP,
constraint idea_pk primary key(iID));



create table subscription(
sID int not null auto_increment,
uID int not null,
iID int not null,
constraint subscription_pk primary key(sID));


create table favcategory(
fID int not null auto_increment,
uID int not null,
cID int not null,
constraint favcategory_pk primary key(fID));



alter table idea  ADD FOREIGN KEY (uID) REFERENCES user(uID);
alter table idea  ADD FOREIGN KEY (cID) REFERENCES category(cID);

alter table subscription  ADD FOREIGN KEY (uID) REFERENCES user(uID);
alter table subscription  ADD FOREIGN KEY (iID) REFERENCES idea(iID);

alter table favcategory  ADD FOREIGN KEY (uID) REFERENCES user(uID);
alter table favcategory  ADD FOREIGN KEY (cID) REFERENCES category(cID);

show tables;


create table room(
rID int not null auto_increment,
iID int not null ,
uID int not null,
name varchar(20) not null unique,
constraint room_pk primary key(rID));
alter table room  ADD FOREIGN KEY (uID) REFERENCES user(uID);
alter table room  ADD FOREIGN KEY (iID) REFERENCES idea(iID);

create table room_members(
rmID int not null auto_increment,
rID int not null ,
iID int not null ,
uID int not null,
constraint roomm_pk primary key(rmID));
alter table room_members  ADD FOREIGN KEY (uID) REFERENCES user(uID);
alter table room_members  ADD FOREIGN KEY (iID) REFERENCES idea(iID);
alter table room_members  ADD FOREIGN KEY (rID) REFERENCES room(rID);

select * from category;
select * from idea;
select count(*), status from idea group by status;
select * from user;
select * from room;
select * from subscription;
select * from room_members;
select * from history;
describe room;

SELECT COUNT(*),cateogry_name FROM category,idea WHERE idea.cID=category.cID;

update idea set status='in-progress' where iID=1;
INSERT INTO idea(uID,idea_desc,cID,title,status) values(4, 'There is something so idyllic about seeing the sky reflected in a body of water. There is a reason why we love seeing that — our eyes are drawn to reflections. So look for opportunities to play with them in photos',
3, 'Playing with Reflections to get amazing Clicks', 'initiated');
INSERT INTO category(cateogry_name) values('Social-Service'),('Photography'),('Music'),('Arts and Crafts');
INSERT INTO category(cateogry_name) values('Healthcare');
insert INTO category(cateogry_name) VALUES ('Technology');

INSERT INTO user(fname,lname,gender,phone,email,passwrd,department) values('Kavita','hegde','Female','9481121732','abc@email.com','Pass@word1','Consulting');
INSERT INTO user(fname,lname,gender,phone,email,passwrd,department) values('Justika','hegde','Female','9481121732','xyz@email.com','Pass@word1','Consulting');
INSERT INTO user(fname,lname,gender,phone,email,passwrd,department,isadmin) values('Kakshi','Hatake','Male','9481121732','kakashi@email.com','Pass@word1','Tax',1);

SELECT idea.title, user.fname,user.lname ,category.cateogry_name,idea.status, count(*)-1 FROM idea INNER JOIN user ON idea.uID = user.uID INNER JOIN  category ON idea.cID = category.cID INNER JOIN  room_members ON idea.iID = room_members.iID GROUP BY idea.title;

create table history(
hID int not null auto_increment,
msg varchar(1500) not null,
created datetime not null DEFAULT CURRENT_TIMESTAMP,
rID int not null,
uID int not null,
uname varchar(50) not null,
constraint room_pk primary key(hID));
alter table history  ADD FOREIGN KEY (rID) REFERENCES room(rID);
alter table history  ADD FOREIGN KEY (uID) REFERENCES user(uID);

SELECT  user.fname, user.lname FROM room_members INNER JOIN user ON room_members.uID=user.uID WHERE rID = 1 group by room_members.uID;
