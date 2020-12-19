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
select * from admin;

insert into admin(email, username, password) values ('websiteadmin@gmail.com', 'admin', 'website1admin1');

select * from admin;


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

select * from category;



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

select * from product;
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
select * from cart;
select count(*) from cart;

select idProduct from cart group by idProduct order by rand() limit 4;
select idProduct from cart where idCustomer in (select idCustomer from cart group by idCustomer);

delete from cart where idProduct = 1;


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

alter table orders add status varchar(30) not null default 'Order Placed';
alter table orders drop column status;

alter table orders modify column orderTime timestamp not null default current_timestamp;

desc orders;
select * from orders;

#show all the tables
show tables;


#insert data into category table
insert into category(categoryName) values ('smartphone'); #for smartphones
insert into category(categoryName) values ('earphones'); #for earphones and headphones
insert into category(categoryName) values ('tshirt'); #for tshirt
insert into category(categoryName) values ('football'); #for football
insert into category(categoryName) values ('volleyball'); #for volleyball
insert into category(categoryName) values ('table'); #for table
insert into category(categoryName) values ('chair'); #for chair
insert into category(categoryName) values ('speaker'); #for speaker
insert into category(categoryName) values ('bags'); #for bags
insert into category(categoryName) values ('caps'); #for caps

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

insert into product(name, cost, description, image, quantityAvailable, categoryName)
    values('Redmi Note 8 Pro', 15490, 'Halo White | 6GB RAM | 128GB Storage', 'redmiNote8Pro.jpg', 10, 'smartphone');

insert into product(name, cost, description, image, quantityAvailable, categoryName)
    values('Redmi 8 Pro', 15490, 'Onyx Black | 4GB RAM | 64GB Storage', 'redmi8.jpg', 10, 'smartphone');

insert into product(name, cost, description, image, quantityAvailable, categoryName)
    values('Apple 11', 56999, 'Green | 8GB RAM | 128GB Storage', 'apple11.jpg', 20, 'smartphone');
insert into product(name, cost, description, image, quantityAvailable, categoryName)
    values('Apple 7', 24999, 'Black | 4GB RAM | 32GB Storage', 'apple7.jpg', 10, 'smartphone');
insert into product(name, cost, description, image, quantityAvailable, categoryName)
    values('Nokia Android 5.3', 12499, 'Charcoal | Quad Camera | 4GB RAM | 64GB Storage', 'nokiaAndroid.jpg', 10, 'smartphone');

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
insert into product(name, cost, description, image, quantityAvailable, categoryName)
    values('Aftershokz Aeropex', 12499, 'Lunar Grey | Open-Ear Wireless Headphones', 'afterShokzAeropex.jpg', 10, 'earphones');
insert into product(name, cost, description, image, quantityAvailable, categoryName)
    values('Noise Shots Rush', 2799, 'Wine Red | Wireless Bluethooth Earbuds', 'noiseShotsRush.jpg', 10, 'earphones');


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

#football
insert into product(name, cost, description, image, quantityAvailable, categoryName)
    values('Nivia Shining Star', 869, 'Football', 'NiviaShiningStarFootball.jpg', 50, 'football');
insert into product(name, cost, description, image, quantityAvailable, categoryName)
    values('SMT Hand Stitched', 399, 'Football | Size-05 | With Pump', 'SMTHandStichedFootballSize05.jpg', 50, 'football');
insert into product(name, cost, description, image, quantityAvailable, categoryName)
    values('Voodania Telstar', 499, 'Football | Combo With Pump', 'voodaniaTelstarCombowithPump.jpg', 50, 'football');
insert into product(name, cost, description, image, quantityAvailable, categoryName)
    values('Cosco Football', 528, 'Football | Cosco Cuba', 'coscoFootball.jpg', 50, 'football');


#volleyball
insert into product(name, cost, description, image, quantityAvailable, categoryName)
    values('Nivia Craters Molded', 415, 'Volleyball', 'NiviaCratersMoldedVolleyball.jpg', 50, 'football');
update product set categoryName='volleyball' where idProduct=28;
insert into product(name, cost, description, image, quantityAvailable, categoryName)
    values('Vector X Spike', 445, 'Volleybal | Rubber Moulded', 'VectorXSpikeRubberMouldedVolleyball.jpg', 50, 'football');
insert into product(name, cost, description, image, quantityAvailable, categoryName)
    values('Cosco Volleyball', 665, 'Volleyball | Size-05', 'coscoVolleyball.jpg', 50, 'volleyball');

select count(*) from product where categoryName='football';

#table
insert into product(name, cost, description, image, quantityAvailable, categoryName)
    values('Solimo Wanderer MultiPurpose Table', 699, 'Laptop Table | Wenge', 'SolimoWandererMultiPurposeTable.jpg', 10, 'table');
insert into product(name, cost, description, image, quantityAvailable, categoryName)
    values('Craftenia Wooden Table', 274, 'Folding Side Table', 'CrafteniaWoodenFoldingSideTable.jpg', 10, 'table');
insert into product(name, cost, description, image, quantityAvailable, categoryName)
    values('Cello Oasis Centre Table', 1130, 'Centre Table', 'CelloOasisCentreTable.jpg', 10, 'table');
insert into product(name, cost, description, image, quantityAvailable, categoryName)
    values('MBTC Lapis Table', 1130, 'Folding Table | Office | Study', 'MBTCLapisFoldingTable.jpg', 10, 'table');
insert into product(name, cost, description, image, quantityAvailable, categoryName)
    values('Cicada Dinning Table', 1130, 'Stainless Steel', 'CicadaPremiumHydraStainlessSteelDinningTable.jpg', 10, 'table');

#chair
insert into product(name, cost, description, image, quantityAvailable, categoryName)
    values('Lakdwood Sofa Chair', 1599, 'Woodenand | Fabric | Backrest', 'LakdwoodWoodenandFabricBackrestAccentSofaChair.jpg', 5, 'chair');
insert into product(name, cost, description, image, quantityAvailable, categoryName)
    values('Faburaa Chair', 799, 'Premium Velvet', 'FaburaaRioPremiumVelvetChair.jpg', 5, 'chair');
insert into product(name, cost, description, image, quantityAvailable, categoryName)
    values('M S Deco Chair', 799, 'Timbers | Parekh', 'MSTimbersAndTheParekhDecoChair.jpg', 5, 'chair');
insert into product(name, cost, description, image, quantityAvailable, categoryName)
    values('Foldable Lounger', 799, 'Comfy Bean Bags | Wine', 'ComfyBeanBagsFoldableLounger.jpg', 5, 'chair');
insert into product(name, cost, description, image, quantityAvailable, categoryName)
    values('Reclining Lounge Chair', 3799, 'Zero Gravity Lounge Chair', 'ZeroGravityRecliningLoungePortableChair.jpg', 5, 'chair');

#speaker
insert into product(name, cost, description, image, quantityAvailable, categoryName)
    values('Zebronics Speaker', 617, 'Bluetooth Speaker', 'ZebronicsZebCountyBluetoothSpeaker.jpg', 10, 'speaker');
insert into product(name, cost, description, image, quantityAvailable, categoryName)
    values('Infinity JBL', 749, 'Bluetooth Speaker | Dual EQ', 'InfinityJBLFuzePintDeepBassDualEQBluetooth.jpg', 10, 'speaker');
insert into product(name, cost, description, image, quantityAvailable, categoryName)
    values('iBall Cube', 516, 'Bluetooth Speaker | Ultra Portable', 'iBallMusiCubeX1WirelessUltraPortableBS.jpg', 10, 'speaker');
insert into product(name, cost, description, image, quantityAvailable, categoryName)
    values('boAt Stone', 516, 'Bluetooth Speaker | Black', 'boAtStone1705WBluetoothSpeaker.jpg', 10, 'speaker');
insert into product(name, cost, description, image, quantityAvailable, categoryName)
    values('Sony SRS-XB23', 8850, 'Bluetooth Speaker | Blue', 'SonySRS_XB23WirelessExtraBassBS.jpg', 10, 'speaker');
insert into product(name, cost, description, image, quantityAvailable, categoryName)
    values('Artis BT90', 8850, 'Bluetooth Speaker | Black', 'ArtisBT90WirelessPortableBluetoothS.jpg', 10, 'speaker');

#bags
insert into product(name, cost, description, image, quantityAvailable, categoryName)
    values('Tool Backpack', 3299, 'Bag | 2 Pockect Front', 'AmazonBasicsTool BagBackpack,.jpg', 10, 'bags');
insert into product(name, cost, description, image, quantityAvailable, categoryName)
    values('OGIO Women\'s Bag', 3299, 'Bag | Casual Backpack', 'OGIOWomensHamptonsWindowpaneH.jpg', 10, 'bags');
insert into product(name, cost, description, image, quantityAvailable, categoryName)
    values('MOCA Laptop Bag', 1299, 'Bag | Laptop', 'MOCABagSleeveAppleMacBook.jpg', 10, 'bags');
insert into product(name, cost, description, image, quantityAvailable, categoryName)
    values('MONCI Bag', 1299, 'Bag | Backpack', 'MONCIMilestoneLaptopBackpacks.jpg', 10, 'bags');
insert into product(name, cost, description, image, quantityAvailable, categoryName)
    values('TH Bag', 999, 'Bag | Backpack', 'TommyHilfigerNavyLaptopBackpack.jpg', 10, 'bags');
insert into product(name, cost, description, image, quantityAvailable, categoryName)
    values('WC Polyester Bag', 1545, 'Bag | Backpack', 'WildcraftTurnaroundPolyesterBlueBag.jpg', 10, 'bags');
insert into product(name, cost, description, image, quantityAvailable, categoryName)
    values('WC Black Bag', 1691, 'Bag | Backpack', 'WildcraftBlackAndMelBackpack .jpg', 20, 'bags');
insert into product(name, cost, description, image, quantityAvailable, categoryName)
    values('Nike', 1469, 'Bag | Backpack', 'NikeObsidianBlackWolfGreyBackpack .jpg', 20, 'bags');
insert into product(name, cost, description, image, quantityAvailable, categoryName)
    values('Nike Handbag', 1460, 'Bag', 'NikeHandbag .jpg', 20, 'bags');
update product set image='WildcraftBlackAndMelBackpack.jpg' where idProduct=52;
#caps
insert into product(name, cost, description, image, quantityAvailable, categoryName)
    values('Ediko Cap', 255, 'Cap | Blue | Free Size', 'EdikoMensMeshSnapbackCap .jpg', 50, 'caps');
insert into product(name, cost, description, image, quantityAvailable, categoryName)
    values('TyranT Cap', 249, 'Cap | Unisex', 'TyranTCap .jpg', 50, 'caps');
update product set image='EdikoMensMeshSnapbackCap.jpg' where idProduct=55;
insert into product(name, cost, description, image, quantityAvailable, categoryName)
    values('ILU NY Cap', 339, 'Cap | Unisex', 'iluNYCap.jpg', 50, 'caps');
insert into product(name, cost, description, image, quantityAvailable, categoryName)
    values('Zacharias Cap ', 499, 'Cap | Neck Muffer | Neck Warmer', 'ZachariasMenWoolenCapwithNeckwarmer.jpg', 50, 'caps');
insert into product(name, cost, description, image, quantityAvailable, categoryName)
    values('Handcuffs Cap ', 399, 'Cap', 'HandcuffsAdjustableCap.jpg', 50, 'caps');
insert into product(name, cost, description, image, quantityAvailable, categoryName)
    values('Handcuffs Sports Cap ', 499, 'Cap | Sports', 'HandcuffsUnisexCap.jpg', 50, 'caps');
insert into product(name, cost, description, image, quantityAvailable, categoryName)
    values('FabSeasons Cap ', 299, 'Cap | Sports', 'FabSeasonsSolidPolyesterGolfFlatCap.jpg', 50, 'caps');


select * from product;
select * from product where idProduct=30;
update product set name='Solimo Table' where idproduct=30;
select image from product;
select * from product where categoryName='caps';
select categoryName, count(*) from product group by categoryName;

select * from product where image='samGalaxyM31.jpg';
select image, name, cost, idProduct from product where idProduct in (1,3);
select image, name, cost, description, categoryName, idProduct from product where idProduct = 1 ;
select categoryName, count(idProduct) from product group by categoryName;

select * from orders;
use labDB;

########### Reports ##########
#1) frequently viewed products to be displayed on the website
	#frequently viewed products are those which are added by the customers to their carts
	#select those products which customers adds to the cart
    #this can be used in the inventory so that the stock of products are met with the user requirements.
select idProduct from cart group by idProduct order by rand() limit 4;
select idProduct from cart group by idProduct order by rand();

#2) select users as per their city, state, or country
	#this can used by the admin to set up stations in real life so that the delivery can be achieved at a fastre rate.
select streetOrvillage, count(streetOrvillage) from customer group by streetOrvillage;
select cityOrTown, count(cityOrTown) from customer group by cityOrTown;
select state, count(state) from customer group by state;
select country, count(country) from customer group by country;

#3 select the number of products a customer has in thier carts

select idCustomer, count(idCustomer) from cart group by idCustomer;

#4 to find which customer has how many products in the cart, also display their respective username
	#the #3 and #4 report can be used to keep up the product stocks in the nearest inventory location to the user
    #this could help in achieving faster delivery
select username from customer where idCustomer in (select distinct idCustomer from cart);

select customer.username, count(cart.idProduct) from 
	customer, cart where customer.idCustomer=cart.idCustomer group by customer.username;

#5 find how many products each customer has ordered

select customer.username, count(orders.idProduct) from 
			customer, orders where customer.idCustomer=orders.idCustomer group by customer.username;
