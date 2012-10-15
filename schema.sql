drop table if exists results;
create table results (
	id integer primary key autoincrement,
	session_id integer not null,
	q1 string not null,
	q2 string not null,
	email string null
);

