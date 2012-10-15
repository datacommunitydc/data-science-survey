drop table if exists entries;

create table entries (
	id integer primary key autoincrement,
	sessionid integer, not null

	email string null,

);

