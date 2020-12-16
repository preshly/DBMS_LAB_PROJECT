#database file for the dbms lab project
#1911

show databases;
use labDB;


#admin table
drop table if exists admin;

create table admin(
	idAdmin int not null auto_increment,
    email varchar(30) not null,
    username varchar(20) not null,
    password varchar(20) not null,
    primary key(idAdmin, email, username)
);

desc admin;


#customer table
drop table if exists customer;

create table customer(
	idCustomer int not null auto_increment,
    email varchar(30) not null,
    firstName varchar(30) not null,
    lastName varchar(30) not null,
    contact varchar(10) not null,
    houseNoOrFlatNo varchar(10) not null,
    streetOrvillage varchar(30) not null,
    cityOrTown varchar(30) not null,
    state varchar(30) not null,
    country varchar(30) not null,
    username varchar(20) not null,
    password varchar(20) not null,
    primary key(idCustomer, email, username)
);

alter table customer modify column password varchar(50) not null;

desc customer;

select * from customer;

delete from  customer where idCustomer=15;

select idCustomer from customer where email='rohit@gmail.com' and username='rohitur';


#category table
drop table if exists category;

create table category(
	categoryName varchar(30) not null,
	primary key(categoryName)
);

desc category;


#product table
drop table if exists product;

create table product(
	idProduct int not null auto_increment,
    name varchar(50) not null,
    cost float not null,
    description varchar(256) not null,
    image varchar(50) not null,
    quantityAvailable int not null,
    categoryName varchar(30) not null,
    primary key(idProduct),
    foreign key(categoryName) references category(categoryName)
);

desc product;


#cart table
drop table if exists cart;

create table cart(
	idCustomer int not null,
    idProduct int not null,
    primary key(idCustomer, idProduct),
    foreign key(idCustomer) references customer(idCustomer),
    foreign key(idProduct) references product(idProduct)
);

desc cart;


#orders table
drop table if exists orders;

create table orders(
	idOrder int not null auto_increment,
    idCustomer int not null,
    idProduct int not null,
    quantity int not null,
    orderTime timestamp not null,
    subTotal float not null,
    remoteIPAddress varchar(16) not null,
    primary key(idOrder, idCustomer, idProduct),
    foreign key(idCustomer) references customer(idCustomer),
    foreign key(idProduct) references product(idProduct)
);

alter table orders add status varchar(30) not null;
alter table orders drop column status;

desc orders;


#show all the tables
show tables;


#insert data into category table
insert into category(categoryName) values ('smartphone'); #for smartphones
insert into category(categoryName) values ('earphones'); #for earphones and headphones
insert into category(categoryName) values ('tshirt'); #for tshirt

select * from category;

# insert data into the product table

#smartphones
insert into product(name, cost, description, image, quantityAvailable, categoryName)
    values('Samsung Galaxy M31', 18999, 'Mirage Blue | 6GB RAM | 128GB Storage', 'samGalaxyM31.jpg', 10, 'smartphone');

insert into product(name, cost, description, image, quantityAvailable, categoryName)
    values('Samsung Galaxy M01', 7299, 'Blue | 3GB RAM | 32GB Storage', 'samGalaxyM01.jpg', 10, 'smartphone');

insert into product(name, cost, description, image, quantityAvailable, categoryName)
    values('OPPO A12', 8990, 'Black | 4GB RAM | 64GB Storage', 'oppoA12.jpg', 15, 'smartphone');

insert into product(name, cost, description, image, quantityAvailable, categoryName)
    values('OPPO A5S', 7499, 'Black | 3GB RAM | 32GB Storage', 'oppoA5s.jpg', 5, 'smartphone');

insert into product(name, cost, description, image, quantityAvailable, categoryName)
    values('VIVO V20', 22990, 'Sunset Melody | 8GB RAM | 128GB Storage', 'vivoV20.jpg', 12, 'smartphone');

insert into product(name, cost, description, image, quantityAvailable, categoryName)
    values('VIVO Y12', 10990, 'Aqua Blue | 3GB RAM | 64GB Storage', 'vivoY12.jpg', 10, 'smartphone');

#earphones
insert into product(name, cost, description, image, quantityAvailable, categoryName)
    values('Zinq Technologies Beatle 5155', 799, 'Black | Super Bass Bluetooth | On-Ear Headphones with Mic', 'zinqTechnologiesBeatle5155.jpg', 20, 'earphones');

insert into product(name, cost, description, image, quantityAvailable, categoryName)
    values('Lumiford Ultimate U20', 499, 'Blue | HD Sound | 10mm Dynamic Drivers for Effective Bass | In-Ear Wired Earphones with Mic | Durable Tangle Free Cable', 'lumifordUltimateU20.jpg', 15, 'earphones');

insert into product(name, cost, description, image, quantityAvailable, categoryName)
    values('JBL C100SI', 599, 'Black | In-Ear Deep Base Headphones with Mic', 'jblC100SI.jpg', 10, 'earphones');

insert into product(name, cost, description, image, quantityAvailable, categoryName)
    values('boAt Rockerz 450', 1499, 'Luscious Black | On-Ear Headphones with Mic', 'boAtRockerz450.jpg', 30, 'earphones');

insert into product(name, cost, description, image, quantityAvailable, categoryName)
    values('Aftershokz Trekz Titanium', 8469, 'Grey | Bone Conduction Bluetooth Headphones with Mic', 'aftershokzTrekzTitanium.jpg', 25, 'earphones');

#tshirt
insert into product(name, cost, description, image, quantityAvailable, categoryName)
    values('EYEBOGLER Men\'s TShirt  ', 320, 'Wine Melange Black | V-Neck Shawl Collar T-Shirt', 'EYEBOGLERVNeckShawlCollarMensTShirt.jpg', 50, 'tshirt');

insert into product(name, cost, description, image, quantityAvailable, categoryName)
    values('Luke And Lilly Boys TShirt  ', 320, 'Yellow White Black | Half Sleeve Cotton Tshirt', 'LukeLillyBoysCutSewHalfSleeveCottonTshirts.jpg', 50, 'tshirt');

insert into product(name, cost, description, image, quantityAvailable, categoryName)
    values('Dagcros Mens TShirt', 449, 'White & Black | Classic Hooded T-Shirt', 'DagcrosMensBoysClassicHoodedTShirt.jpg', 50, 'tshirt');

insert into product(name, cost, description, image, quantityAvailable, categoryName)
    values('Innovative Edge Men\'s TShirt', 389, 'Black | Classic Fit T-Shirt', 'innovativeEdgeMensClassicFitTShirt.jpg', 50, 'tshirt');

insert into product(name, cost, description, image, quantityAvailable, categoryName)
    values('Elk Men\'s TShirt', 629, 'Grey | Full Sleeve Round Neck', 'ElkBoysTShirt.jpg', 50, 'tshirt');


select * from product;

use labDB;

