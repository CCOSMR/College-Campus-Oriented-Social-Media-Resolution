-- New user sign up
INSERT INTO User (id, password, email, time_joined, name)
VALUES ("malcom1466", "IHATEPEWDIEPIE", "malcom1466@malcom.com", DATETIME("now"), "Pewds Slayer Malcom1466");

-- Edit user description
update User
set dscr = "pewdiepie #sucks #hate #felix #broarmy"
where id = "malcom1466";

-- Follow
INSERT INTO Follow (following_id, follower_id, time_followed)
VALUES ("pewdiepie", "malcom1466", DATETIME("now"));

-- Get user password
select password from User where id = "malcom1466";