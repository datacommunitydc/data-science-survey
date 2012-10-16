drop table if exists results;
create table results (
	id integer primary key autoincrement,
	session_id integer not null,
	q1 string not null,
	q2 string not null,
	email integer null
);

create table results (
	session_id int not null,
	q1 varchar not null,
	q2 varchar not null,
	email varchar null
);
