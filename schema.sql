DROP TABLE IF EXISTS user;
CREATE TABLE user(
  uid integer primary key autoincrement,
	email text not null,
	facebook_id text not null,
	twitter_id text not null,
	google_plus_id text not null,
	hashed_password text not null
);

DROP TABLE IF EXISTS mood;
CREATE TABLE mood(
  id integer primary key autoincrement,
  mood integer not null,
  lat real null,
  long real null
);
