
create table City (
  id integer not null primary key,
  name varchar(255),
  country varchar(255)
);
 
create table University (
  id integer not null primary key,
  city_id integer,
  name varchar(255) not null unique,
  dscr Varchar(4096),
  website varchar(1024),
  foreign key(city_id) references City(id)
);
 
create table Users (
  id varchar(64) not null primary key,
  password varchar(64),
  email varchar(255) unique, -- constraint user_email_format check (prefix REGEXP '^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$'),
  time_joined datetime,
  type integer,
  activity real,
  name varchar(255),
  dscr varchar(4096)
);
 
create table Follow (
  following_id varchar(64),
  follower_id varchar(64),
  time_followed datetime,
  seen bool,
  primary key (following_id, follower_id),
  foreign key (following_id) references Users(id),
  foreign key (follower_id) references Users(id),
  constraint avoid_self_following check (following_id != follower_id)
);

create table Sub ( -- submission
  id integer not null primary key,
  poster_id integer,
  time_posted datetime,
  publicity integer not null default 0,
  likes integer default 0,
  dislikes integer default 0,
  comments integer default 0,
  foreign key (poster_id) references Users(id)
);

create table Post (
  id integer primary key,
  content varchar(25536),
  foreign key (id) references Sub(id)
);

create table Comments (
  id integer primary key,
  original_id integer,
  content varchar(4096),
  seen bool,
  foreign key (id) references Sub(id),
  foreign key (original_id) references Sub(id),
  constraint avoid_self_comment check (id != original_id)
);

create table Likes (
  sub_id integer,
  user_id integer,
  time_liked datetime,
  seen bool,
  primary key (sub_id, user_id),
  foreign key (sub_id) references Sub(id),
  foreign key (user_id) references Users(id)
);

create table Dislikes (
  sub_id integer,
  user_id integer,
  time_liked datetime,
  primary key (sub_id, user_id),
  foreign key (sub_id) references Sub(id),
  foreign key (user_id) references Users(id)
);

create table College (
  id integer not null primary key,
  university_id integer,
  name varchar(255),
  dscr varchar(4096),
  foreign key (university_id) references University(id)
);

create table Teacher (
  id integer not null primary key,
  college_id integer,
  name varchar(255),
  dscr varchar(4096),
  ave_rating real,
  title varchar(64),
  foreign key (college_id) references College(id)
);

create table Course (
  id integer not null primary key,
  teacher_id integer not null,
  name varchar(255),
  dscr varchar(4096),
  ave_rating real,
  location varchar(255),
  schedule varchar(255),
  foreign key (teacher_id) references Teacher(id)
);

create table Users_Student (
  user_id integer primary key,
  college_id INTEGER,
  date_enrolled date,
  student_id integer,
  student_username varchar(255),
  student_password varchar(255),
  status varchar(255),
  review_quality real,
  foreign key (user_id) references Users(id),
  foreign key (college_id) references College(id)
);

create table Attend (
  student_id integer not null,
  course_id INTEGER not null,
  date_begin date,
  date_end date check (date_end >= date_begin),
  primary key (student_id, course_id),
  foreign key (student_id) references Users_Sutdent(user_id),
  foreign key (course_id) references Course(id)
);

create table Review (
  id integer not null primary key,
  user_id INTEGER,
  course_id integer,
  content varchar(25536),
  rating integer,
  anonymous bool not null,
  seen bool,
  quality real,
  foreign key (id) references Sub(id),
  foreign key (user_id) references Users(id)
);

create table Users_Teacher (
  user_id integer unique,
  teacher_id INTEGER unique,
  date_registered date,
  foreign key (user_id) references Users(id),
  foreign key (teacher_id) references Teacher(id)
);

create table Tag (
  id varchar(255) not null primary key,
  statistics integer
);

create table Mention (
  user_id integer not null,
  sub_id integer not null,
  position integer Not null check (position >= 0),
  seen bool,
  Primary key (user_id, sub_id, position),
  foreign key (user_id) references Users(id),
  foreign key (sub_id) references Sub(id)
);

create table Tag_Usage (
  tag integer not null,
  sub_id integer not null,
  position integer Not null check (position >= 0),
  primary key (tag, sub_id, position),
  foreign key (tag) references Tag(tag),
  foreign key (sub_id) references Sub(id)
);