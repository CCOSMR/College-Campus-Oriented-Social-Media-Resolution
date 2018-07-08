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

-- Get 5 post ids
	--  Needs modification
select poster_id, time_posted, likes, dislikes, comments from Sub where
	id = (
		select post_id from 
			select count(5) from
				select id as post_id from Post where 
					post_id = (
						select id as sub_id, time_posted from Sub where	
						post_id = sub_id and 
						time_posted < (
							select time_posted from Sub where id = "last_post_id"
						) and
						poster_id = (
							select following_id from Follow where	
							follower_id = "user_id"
						)
					)
				union select id as post_id from Review where 
					post_id = (
						select id as sub_id, time_posted from Sub where	
						post_id = sub_id and 
						time_posted < (
							select time_posted from Sub where id = "last_post_id"
						) and
						poster_id = (
							select following_id from Follow where	
							follower_id = "user_id"
						)
					)
				union select id as post_id from Post where 
					post_id = (select id as sub_id, time_posted from Sub where	
						post_id = sub_id and 
						time_posted > "refreshed_time" and
						poster_id = (
							select following_id from Follow where	
							follower_id = "user_id"
						)
					);
				union select id as post_id from Review where 
					post_id = (select id as sub_id, time_posted from Sub where	
						post_id = sub_id and 
						time_posted > "refreshed_time" and
						poster_id = (
							select following_id from Follow where	
							follower_id = "user_id"
						)
					);
		)
-- Get post information
