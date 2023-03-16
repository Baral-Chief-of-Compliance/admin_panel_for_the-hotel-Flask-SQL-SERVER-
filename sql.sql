create database GLEB;

use GLEB;

create table Operator(
	id int primary key,
    login varchar(50),
    pass_hash varchar(256)
);

insert into operator values (1, 'admin', '$2b$13$QZFUfMkVowrZL1XDi.rOvuZN.IQCjJqt2M5rjXnLKIqtoSCC1hwMm');
insert into Организация values (0, 'нет', 'нет', 0);
insert into клиент values (0, 'нет', 'нет', 'нет', 0);

create table доп_услуги(
	номер_услуги int primary key,
    вид_услуги varchar(50),
    стоимость_у decimal(15,2)
);


create table клиент(
	номер_клиента int primary key,
    фамилия_к varchar(50),
    имя_к varchar(50),
    отчество_к varchar(50),
    банковский_счет_к varchar(50)
);

create table гостиничный_комплекс(
	номер_здания int,
    номер_комнаты varchar(10),
    primary key(номер_здания, номер_комнаты),
    этаж int,
    местность int,
    классность int,
    стоимость_н decimal(15,2),
    статус_номера varchar(50)
);


create table Менеджер(
	номер_менеджера int primary key,
    фамилия_м varchar(50),
    имя_м varchar(50),
    отчество_м varchar(50)
);


create table Организация (
	номер_организации int primary key,
    название_орг varchar(50),
    тип_орг varchar(50),
    банковский_счет_о varchar(50)
);


create table договор(
	номер_договора varchar(50) primary key,
    номер_организации int,
    номер_клиента int,
    номер_менеджера int,
    количество_чел int,
    номер_здания int,
    номер_комнаты varchar(50),
    дата_заселения date,
    дата_выселения date,
    foreign key (номер_организации) references Организация(номер_организации) on delete cascade on update cascade,
    foreign key (номер_клиента) references клиент(номер_клиента) on delete cascade on update cascade,
    foreign key (номер_менеджера) references Менеджер(номер_менеджера) on delete cascade on update cascade,
    foreign key (номер_здания, номер_комнаты) references гостиничный_комплекс(номер_здания, номер_комнаты) on delete cascade on update cascade
);


create table история_обслуживания(
	номер_договора varchar(50),
    номер_чека int,
    номер_услуги int,
    статус_оплаты varchar(50),
    primary key(номер_договора, номер_чека),
    foreign key (номер_договора) references договор(номер_договора) on delete cascade on update cascade,
	foreign key (номер_услуги) references доп_услуги(номер_услуги) on delete cascade on update cascade
);


select * from доп_услуги;
insert into доп_услуги value (1, 'уборка комнаты', 5000);
insert into доп_услуги value (2, 'посещение бассейна', 6000);
insert into доп_услуги value (3, 'посещение сауны', 5000);
insert into доп_услуги value (4, 'завтрак в номер', 10000);
insert into доп_услуги value (5, 'аренда автомобиля', 5000);
insert into доп_услуги value (6, 'посещение спортзала', 15000);
insert into доп_услуги value (7, 'массаж в номере', 20000);
insert into доп_услуги value (8, 'бильярд', 4000);
insert into доп_услуги value (9, 'теннисный корт', 6000);
insert into доп_услуги value (10, 'дегустация вина', 10000);
insert into менеджер value (1, 'Павлов', 'Александр', 'Тихонович');

insert into гостиничный_комплекс values (1, '1A', 1,2,1,2000,'занято');
insert into гостиничный_комплекс values (1, '1B', 2,3,2,3000,'занято');
insert into гостиничный_комплекс values (1, '2A', 1,2,1,2000,'занято');
insert into гостиничный_комплекс values (1, '2B', 2,3,2,3000,'не занято');
insert into гостиничный_комплекс values (1, '3A', 1,2,1,2000,'занято');
insert into гостиничный_комплекс values (1, '3B', 2,3,2,3000,'занято');
insert into гостиничный_комплекс values (2, '1A', 1,5,3,6000,'не занято');
insert into гостиничный_комплекс values (2, '1B', 2,4,3,7000,'занято');
insert into гостиничный_комплекс values (3, '3A', 1,3,2,5000,'занято');
insert into гостиничный_комплекс values (4, '4A', 1,1,3,10000,'не занято');
insert into гостиничный_комплекс values (5, '4C', 3,1,2,6000,'не занято');
