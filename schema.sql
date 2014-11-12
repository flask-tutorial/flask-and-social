DROP TABLE IF EXISTS user;
CREATE TABLE user(
  uid integer primary key autoincrement,
	email text null,
	facebook_id text null,
	twitter_id text null,
	google_plus_id text null,
	hashed_password text null
);
INSERT INTO user (uid,email) VALUES(1,"bjelli@gmail.com");

DROP TABLE IF EXISTS mood;
CREATE TABLE mood(
  mid integer primary key autoincrement,
  uid integer not null,
  mood integer not null,
  lat real null,
  long real null
);
