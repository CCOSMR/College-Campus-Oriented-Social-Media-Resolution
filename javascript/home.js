var latest_post_time_stamp = Date.now();
var earliest_post_time_stamp = Date.now();
var subs = []
var self_id, self_name;

const monthNames = ["January", "February", "March", "April", "May", "June",
  "July", "August", "September", "October", "November", "December"
];

$(function() {
	var data = 0;
	$.post("/self",
			data,
			function(response){
				self_id = response['id'];
				self_name = response['name'];
				$('#self_name').text(self_name);
				$('#self_id').text('@' + self_id);
				$('#self_picture').html(`<img id='self_picture' style="border-radius: 50%; height:50px;"
										src="/static/pictures/` + self_id + '">');
			});
});

$(function() {
	$('.button-like').on('click', function () {
		$(this).toggleClass("liked");
	});
});

$(function() {
	$("#refresh_button").hover(function(){
		$("#refresh_icon").addClass("hover");
		}, function() {
		  $("#refresh_icon").removeClass("hover");
	});
});

$(function() {
	// request messages
	// insert 
});

jQuery(function($) {
	jQuery(window).scroll(function(){
	 var ScrollTop = jQuery(window).scrollTop();
	 var data;
	 var data = JSON.stringify({
		"earliest_post_time_stamp": earliest_post_time_stamp,
		"latest_post_time_stamp": latest_post_time_stamp,
		"type":"backward",
		"user":"",
	});
	 
	 if ($(this).scrollTop() + $(window).innerHeight() + 1 >= $("#content-wrapper").innerHeight()) { 
		
	  $.post("/request_posts",
			data,
			function(response){
				$(function() {
					for (var i = 0; i < response.length; i++) {
						insert_post(response[i].post_id, response[i].poster_id, response[i].poster_name, response[i].time, 
							response[i].content, response[i].likes, response[i].dislikes, response[i].comments, response[i].liked, response[i].disliked);
						
					}
					earliest_post_time_stamp = response['timestamp'];
				});
			});
	 }
	 });
	 
});

function check_post() {
	 var ScrollTop = jQuery(window).scrollTop();
	 var data;
	 var data = JSON.stringify({
		"earliest_post_time_stamp": earliest_post_time_stamp,
		"latest_post_time_stamp": latest_post_time_stamp,
		"type":"backward",
		"user":"",
	});
	 
	 if ($(this).scrollTop() + $(window).innerHeight() + 1 >= $("#content-wrapper").innerHeight()) { 
		
	  $.post("/request_posts",
			data,
			function(response){
				for (var i = 0; i < response.length; i++) {
					insert_post(response[i].post_id, response[i].poster_id, response[i].poster_name, response[i].time, 
						response[i].content, response[i].likes, response[i].dislikes, response[i].comments, response[i].liked, response[i].disliked);
					
				}
				earliest_post_time_stamp = response['timestamp'];
				latest_post_time_stamp = Date.now();
			});
	 }
	 
	 
	 time_stamp = Date.now();
}

function load_recent_posts() {
	var earliest_post_time_stamp = earliest_post_time_stamp;
	var latest_post_time_stamp = latest_post_time_stamp;
	var data;
	var data = JSON.stringify({
		"earliest_post_time_stamp": time_stamp,
		"latest_post_time_stamp": latest_post_time_stamp,
		"type":"forward",
		"user":"",
	});
	$.post("/request_posts",
		data,
		function(response){
			for (var i = 0; i < response.length; i++) {
				prepend_post(response[i].post_id, response[i].poster_id, response[i].poster_name, response[i].time, 
					response[i].content, response[i].likes, response[i].dislikes, response[i].comments, response[i].liked, response[i].disliked);
				
			}
			latest_post_time_stamp = Date.now();
		});
	
}
function insert_post(post_id, poster_id, poster_name, time, content, likes, dislikes, comments, liked, disliked) {
	subs[post_id] = {'type': 'post', 'liked': liked, 'disliked': disliked, 'comments': comments};
	var date = new Date(time*1000);
	var time_string = ' ' +(date.getDay() + 1) + ', ' 
                  + monthNames[date.getMonth()] + ', '
                  + date.getFullYear();
				  
	new_post = 
	`<div class='post_div' id="` + post_id + `"><article class="excerpt">
		<div id="post" class="excerpttxt" style="padding:15px;">
			<ul class="nospace inline pushright font-xs">
				<li>
					<img src="/static/pictures/` + post_id + `" style="border-radius: 50%; height:40px;">
					</img>
				</li>
				<ul class="nospace inline pushright font-xs">
					<li><h6 id="poster_name" class="heading">`+ poster_name + `</h6></li>
					<ul class="nospace inline pushright font-xs"> 
						<li><a id="poster_id" href="/user=` + poster_id + `">` + "@" + poster_id + `</a></li>
						<li id="time" ><i class="fa fa-calendar-o"></i>` + time_string + `</li>
					</ul>
				</ul>
			</ul>
			<p>` + content + `</p>
			<ul class="nospace inline pushright font-xs">
			  <li><button class="button button-like" id="like_button" onclick="click_like(` + post_id + `);">
					<i class="fa fa-heart"></i>
					<span id="likes" >` + likes + `</span>
					</button> </li>
			  <li><button class="button button-dislike" id="dislike_button" onclick="click_dislike(` + post_id + `);">
					<i class="fa fa-thumbs-down"></i>
					<span id="dislikes" >` + dislikes + `</span>
					</button> </li>
			  <li><button class="button button-comment" id="comment_button" onclick="click_comment(` + post_id + `);">
					<i class="fa fa-comment"></i>
					<span id="comments" >` + comments + `</span>
					</button> </li>
			  <li><button class="button button-normal"  id="reply_button" onclick="click_reply(` + post_id + `);">
					<i class="fa fa-pencil-square-o"></i>
					<span>Reply</span>
					</button> </li>
			  <li><button class="button button-normal">
					<i class="fa fa-share"></i>
					<span>Share</span>
					</button> </li>
			</ul>
		</div>
		<div id='reply' style="padding-top: 0;padding-left: 15px; display: none;">
			<fieldset>
				<legend class="font-xs">Reply</legend>
				<textarea class="form-control" id="reply_text" rows="2" style:"font-size:.8rem;"></textarea>
				<button type="submit" class="btn btn-primary button-s" onclick="submit_comment(` + post_id + `);">Submit</button>
			</fieldset>
		</div>
		<div id="comments" style="padding-top: 0;padding-left: 15px; display: none;">
			<fieldset>
				<legend class="font-xs">Comments</legend>
				<blockquote>
				</blockquote>
			</fieldset>
		</div>
	</article></div>  `;
	
	document.getElementById('posts_list').innerHTML += new_post;
	if (subs[post_id]['liked']) {
		$('#' + post_id + ' #like_button').toggleClass("liked");
	}
	if (subs[post_id]['disliked']) {
		$('#' + post_id + ' #dislike_button').toggleClass("disliked");
	}
	
}

function prepend_post(post_id, poster_id, poster_name, time, content, likes, dislikes, comments, liked, disliked) {
	subs[post_id] = {'type': 'post', 'liked': liked, 'disliked': disliked, 'comments': comments};
	var date = new Date(time*1000);
	var time_string = ' ' +(date.getDay() + 1) + ', ' 
                  + monthNames[date.getMonth()] + ', '
                  + date.getFullYear();
				  
	new_post = 
	`<div class='post_div' id="` + post_id + `"><article class="excerpt">
		<div id="post" class="excerpttxt" style="padding:15px;">
			<ul class="nospace inline pushright font-xs">
				<li>
					<img src="/static/pictures/` + poster_id + `" style="border-radius: 50%; height:40px;">
					</img>
				</li>
				<ul class="nospace inline pushright font-xs">
					<li><h6 id="poster_name" class="heading">`+ poster_name + `</h6></li>
					<ul class="nospace inline pushright font-xs"> 
						<li></i> <a id="poster_id"  href="/user=` + poster_id + `">` + "@" + poster_id + `</a></li>
						<li id="time" ><i class="fa fa-calendar-o"></i>` + time_string + `</li>
					</ul>
				</ul>
			</ul>
			<p>` + content + `</p>
			<ul class="nospace inline pushright font-xs">
			  <li><button class="button button-like" id="like_button" onclick="click_like(` + post_id + `);">
					<i class="fa fa-heart"></i>
					<span id="likes" >` + likes + `</span>
					</button> </li>
			  <li><button class="button button-dislike" id="dislike_button" onclick="click_dislike(` + post_id + `);">
					<i class="fa fa-thumbs-down"></i>
					<span id="dislikes" >` + dislikes + `</span>
					</button> </li>
			  <li><button class="button button-comment" id="comment_button" onclick="click_comment(` + post_id + `);">
					<i class="fa fa-comment"></i>
					<span id="comments" >` + comments + `</span>
					</button> </li>
			  <li><button class="button button-normal"  id="reply_button" onclick="click_reply(` + post_id + `);">
					<i class="fa fa-pencil-square-o"></i>
					<span>Reply</span>
					</button> </li>
			  <li><button class="button button-normal">
					<i class="fa fa-share"></i>
					<span>Share</span>
					</button> </li>
			</ul>
		</div>
		<div id='reply' style="padding-top: 0;padding-left: 15px; display: none;">
			<fieldset>
				<legend class="font-xs">Reply</legend>
				<textarea class="form-control" id="reply_text" rows="2" style:"font-size:.8rem;"></textarea>
				<button type="submit" class="btn btn-primary button-s" onclick="submit_comment(` + post_id + `);">Submit</button>
			</fieldset>
		</div>
		<div id="comments" style="padding-top: 0;padding-left: 15px; display: none;">
			<fieldset>
				<legend class="font-xs">Comments</legend>
				<blockquote>
				</blockquote>
			</fieldset>
		</div>
	</article></div>  `
	
	document.getElementById('posts_list').innerHTML = new_post + document.getElementById('posts_list').innerHTML;
	if (subs[post_id]['liked']) {
		$('#' + post_id + ' #like_button').toggleClass("liked");
	}
	if (subs[post_id]['disliked']) {
		$('#' + post_id + ' #dislike_button').toggleClass("disliked");
	}
}

function click_like(post_id) {
	if (subs[post_id]['disliked'] && !subs[post_id]['liked']) {
		// Cancel the dislike then add like
		var data = JSON.stringify({"post_id": post_id, "like": true, "dislike": false});
		$.post("/like",
			data,
			function(response){
				if (!response['status']) {
					alert('Something went wrong');
				}
				else {
					subs[post_id]['liked'] = true;
					subs[post_id]['disliked'] = false;
					$('#' + post_id + ' #dislike_button').toggleClass("disliked");
					$('#' + post_id + ' #like_button').toggleClass("liked");
					var likes = $('#' + post_id + ' #likes')[0];
					var dislikes = $('#' + post_id + ' #dislikes')[0];
					likes.textContent = parseInt(likes.textContent) + 1;
					dislikes.textContent = parseInt(dislikes.textContent) - 1;
				}
			});
	}
	else if (!subs[post_id]['liked']) {
		// Add a like
		var data = JSON.stringify({"post_id": post_id, "like": true, "dislike": false});
		$.post("/like",
			data,
			function(response){
				if (!response['status']) {
					alert('Something went wrong');
				}
				else {
					subs[post_id]['liked'] = true;
					subs[post_id]['disliked'] = false;
					$('#' + post_id + ' #like_button').toggleClass("liked");
					var likes = $('#' + post_id + ' #likes')[0];
					var dislikes = $('#' + post_id + ' #dislikes')[0];
					likes.textContent = parseInt(likes.textContent) + 1;
				}
			});
	}
	else if (subs[post_id]['liked']) {
		// Cancel the like
		var data = JSON.stringify({"post_id": post_id, "like": false, "dislike": false});
		$.post("/like",
			data,
			function(response){
				if (!response['status']) {
					alert('Something went wrong');
				}
				else {
					subs[post_id]['liked'] = false;
					subs[post_id]['disliked'] = false;
					$('#' + post_id + ' #like_button').toggleClass("liked");
					var likes = $('#' + post_id + ' #likes')[0];
					var dislikes = $('#' + post_id + ' #dislikes')[0];
					likes.textContent = parseInt(likes.textContent) - 1;
				}
			});
	}
	else {
		alert('Something went wrong');
	}
}

function click_dislike(post_id) {
	if (subs[post_id]['liked'] && !subs[post_id]['disliked']) {
		// Cancel the like then add dislike
		var data = JSON.stringify({"post_id": post_id, "like": false, "dislike": true});
		$.post("/like",
			data,
			function(response){
				if (!response['status']) {
					alert('Something went wrong');
				}
				else {
					subs[post_id]['liked'] = false;
					subs[post_id]['disliked'] = true;
					$('#' + post_id + ' #dislike_button').toggleClass("disliked");
					$('#' + post_id + ' #like_button').toggleClass("liked");
					var likes = $('#' + post_id + ' #likes')[0];
					var dislikes = $('#' + post_id + ' #dislikes')[0];
					likes.textContent = parseInt(likes.textContent) -1;
					dislikes.textContent = parseInt(dislikes.textContent) + 1;
				}
			});
	}
	else if (!subs[post_id]['disliked']) {
		// Add a dislike
		var data = JSON.stringify({"post_id": post_id, "like": false, "dislike": true});
		$.post("/like",
			data,
			function(response){
				if (!response['status']) {
					alert('Something went wrong');
				}
				else {
					subs[post_id]['liked'] = false;
					subs[post_id]['disliked'] = true;
					$('#' + post_id + ' #dislike_button').toggleClass("disliked");
					var likes = $('#' + post_id + ' #likes')[0];
					var dislikes = $('#' + post_id + ' #dislikes')[0];
					dislikes.textContent = parseInt(dislikes.textContent) + 1;
				}
			});
	}
	else if (subs[post_id]['disliked']) {
		// Cancel the dislike
		var data = JSON.stringify({"post_id": post_id, "like": false, "dislike": false});
		$.post("/like",
			data,
			function(response){
				if (!response['status']) {
					alert('Something went wrong');
				}
				else {
					subs[post_id]['liked'] = false;
					subs[post_id]['disliked'] = false;
					$('#' + post_id + ' #dislike_button').toggleClass("disliked");
					var likes = $('#' + post_id + ' #likes')[0];
					var dislikes = $('#' + post_id + ' #dislikes')[0];
					dislikes.textContent = parseInt(dislikes.textContent) - 1;
				}
			});
	}
	else {
		alert('Something went wrong');
	}
}

function click_comment(post_id) {
	$('#' + post_id + ' #comment_button').toggleClass("showing");
	if ($('#' + post_id + ' #comment_button').closest('div.post_div').find('div#comments')[0].style.display === "none") {
		$('#' + post_id + ' #comment_button').closest('div.post_div').find('div#comments')[0].style.display = "block";
	} 
	else {
		$('#' + post_id + ' #comment_button').closest('div.post_div').find('div#comments')[0].style.display = "none";
	}
	$('#' + post_id + '.post_div #comments fieldset blockquote').empty();
	get_comments(post_id);
}

function click_reply(post_id) {
	$('#' + post_id + ' #reply_button').toggleClass("clicked");
	if ($('#' + post_id + ' #reply')[0].style.display === "none") {
		$('#' + post_id + ' #reply')[0].style.display = "block";
	} 
	else {
		$('#' + post_id + ' #reply')[0].style.display = "none";
	}
}

function click_reply_small(post_id) {
	$('#' + post_id + ' #reply_button_small').toggleClass("clicked-small");
	if ($('#' + post_id + ' #reply')[0].style.display === "none") {
		$('#' + post_id + ' #reply')[0].style.display = "block";
	} 
	else {
		$('#' + post_id + ' #reply')[0].style.display = "none";
	}
}

function submit_comment(post_id) {
	var time = Date.now() / 1000;
	var content = $('#' + post_id + ' #reply_text').val();
	var data = JSON.stringify({"parent_id": post_id,
	"time_stamp": time, 
	"content": content,
	"visibility": "public"});
	$.post("/comment",
		data,
		function(response){
			if (response['status']) {
				$('#' + post_id + ' #reply_text').val('');
				$('#' + post_id + ' #reply_button').toggleClass("clicked");
				$('#' + post_id + ' #reply')[0].style.display = "none";
				if ($('#' + post_id + ' div#comments')[0].style.display === "none") {
					click_comment(post_id);
				}
				
				var comments = $('#' + post_id + ' #comments')[0];
				comments.textContent = parseInt(comments.textContent) + 1;
			}
			else {
				alert('Failed');
			}
		});
}

function submit_subcomment(post_id) {
	var time = Date.now() / 1000;
	var content = $('#' + post_id + ' #reply_text').val();
	var data = JSON.stringify({"parent_id": post_id,
	"time_stamp": time, 
	"content": content,
	"visibility": "public"});
	$.post("/comment",
		data,
		function(response){
			if (response['status']) {
				$('#' + post_id + ' #reply_text').val('');
				$('#' + post_id + ' #reply_button_small').toggleClass("clicked-small");
				$('#' + post_id + ' #reply')[0].style.display = "none";
				if ($('#' + post_id + ' div#subcomments')[0].style.display === "none") {
					click_comment_small(post_id);
				}
					
				var comments = $('#' + post_id + ' #comments')[0];
				comments.textContent = parseInt(comments.textContent) + 1;
			}
			else {
				alert('Failed');
			}
		});
}

function insert_comment(post_id, comment_id, commenter_id, commenter_name, time, content, likes, dislikes, comments, liked, disliked) {
	subs[comment_id] = {'type': 'comment', 'liked': liked, 'disliked': disliked, 'comments': comments};
	var date = new Date(time*1000);
	var time_string = ' ' +(date.getDay() + 1) + ', ' 
                  + monthNames[date.getMonth()] + ', '
                  + date.getFullYear();
	var new_comment = 
	`<div id="` + comment_id + `" class="excerpttxt" style="padding-right:10px;">
		<ul class="nospace inline pushright font-xs">
			<li>
				<img src="/static/pictures/` + commenter_id + `" style="border-radius: 50%; height:18px;">
				</img>
			</li>
			<li>
				<ul class="nospace inline pushright font-xs">
					<li><h6 class="font-xxs">`+ commenter_name + `</h6></li>
					<ul class="nospace inline pushright"> 
						<li></i> <a class="font-xxs" href="/user=` + commenter_id + `">` + "@" + commenter_id + `</a></li>
						<li class="font-xxs"><i class="fa fa-calendar-o"></i>` + time_string + `</li>
					</ul>
				</ul>
			</li>
		</ul>
		<p class="font-xs">` + content + `</p>
		<ul class="nospace inline pushright font-xxs" style="margin-top: -20px;">
		  <li><button class="button button-like-small" id="like_button_small" onclick="click_like_small(` + comment_id + `);">
				<i class="fa fa-heart"></i>
				<span id="likes">` + likes + `</span>
				</button> </li>
		  <li><button class="button button-dislike-small" id="dislike_button_small" onclick="click_dislike_small(` + comment_id + `);">
				<i class="fa fa-thumbs-down"></i>
				<span id="dislikes">` + dislikes + `</span>
				</button> </li>
		  <li><button class="button button-comment-small" id="comment_button_small" onclick="click_comment_small(` + comment_id + `);">
				<i class="fa fa-comment"></i>
				<span id="comments">` + comments + `</span>
				</button> </li>
		  <li><button class="button button-normal-small" onclick="click_reply_small(` + comment_id + `);"
				<i class="fa fa-pencil-square-o"></i>
				<span>Reply</span>
				</button> </li>
		  <li><button class="button button-normal-small">
				<i class="fa fa-share"></i>
				<span>Share</span>
				</button> </li>
		</ul>
		<div id='reply' style="padding-top: 0;padding-left: -2rem; display: none;">
			<textarea class="form-control" id="reply_text" rows="2" style:"font-size:.8rem;"></textarea>
			<button type="submit" class="btn btn-primary button-s" onclick="submit_subcomment(` + comment_id + `);">Submit</button>
		</div>
		<div id="subcomments" style="padding-top: 0;padding-left: -2rem; display:none;">
			<blockquote>
			</blockquote>
		</div>
		<div id='reply' style='display:none;'>
		</div>
	</div>`
	selector = $('#' + post_id + '.post_div #comments fieldset blockquote')[0];
	selector.innerHTML += new_comment
	if (subs[comment_id]['liked']) {
		$('#' + comment_id + ' #like_button_small').toggleClass("liked-small");
	}
	if (subs[comment_id]['disliked']) {
		$('#' + comment_id + ' #dislike_button_small').toggleClass("disliked-small");
	}
	
}


function click_like_small(post_id) {
	if (subs[post_id]['disliked'] && !subs[post_id]['liked']) {
		// Cancel the dislike then add like
		var data = JSON.stringify({"post_id": post_id, "like": true, "dislike": false});
		$.post("/like",
			data,
			function(response){
				if (!response['status']) {
					alert('Something went wrong');
				}
				else {
					subs[post_id]['liked'] = true;
					subs[post_id]['disliked'] = false;
					$('#' + post_id + ' #dislike_button_small').first().toggleClass("disliked-small");
					$('#' + post_id + ' #like_button_small').first().toggleClass("liked-small");
					var likes = $('#' + post_id + ' #likes')[0];
					var dislikes = $('#' + post_id + ' #dislikes')[0];
					likes.textContent = parseInt(likes.textContent) + 1;
					dislikes.textContent = parseInt(dislikes.textContent) - 1;
				}
			});
	}
	else if (!subs[post_id]['liked']) {
		// Add a like
		var data = JSON.stringify({"post_id": post_id, "like": true, "dislike": false});
		$.post("/like",
			data,
			function(response){
				if (!response['status']) {
					alert('Something went wrong');
				}
				else {
					subs[post_id]['liked'] = true;
					subs[post_id]['disliked'] = false;
					$('#' + post_id + ' #like_button_small').first().toggleClass("liked-small");
					var likes = $('#' + post_id + ' #likes')[0];
					var dislikes = $('#' + post_id + ' #dislikes')[0];
					likes.textContent = parseInt(likes.textContent) + 1;
				}
			});
	}
	else if (subs[post_id]['liked']) {
		// Cancel the like
		var data = JSON.stringify({"post_id": post_id, "like": false, "dislike": false});
		$.post("/like",
			data,
			function(response){
				if (!response['status']) {
					alert('Something went wrong');
				}
				else {
					subs[post_id]['liked'] = false;
					subs[post_id]['disliked'] = false;
					$('#' + post_id + ' #like_button_small').first().toggleClass("liked-small");
					var likes = $('#' + post_id + ' #likes')[0];
					var dislikes = $('#' + post_id + ' #dislikes')[0];
					likes.textContent = parseInt(likes.textContent) - 1;
				}
			});
	}
	else {
		alert('Something went wrong');
	}
}

function click_dislike_small(post_id) {
	if (subs[post_id]['liked'] && !subs[post_id]['disliked']) {
		// Cancel the like then add dislike
		var data = JSON.stringify({"post_id": post_id, "like": false, "dislike": true});
		$.post("/like",
			data,
			function(response){
				if (!response['status']) {
					alert('Something went wrong');
				}
				else {
					subs[post_id]['liked'] = false;
					subs[post_id]['disliked'] = true;
					$('#' + post_id + ' #dislike_button_small').first().toggleClass("disliked-small");
					$('#' + post_id + ' #like_button_small').first().toggleClass("liked-small");
					var likes = $('#' + post_id + ' #likes')[0];
					var dislikes = $('#' + post_id + ' #dislikes')[0];
					likes.textContent = parseInt(likes.textContent) -1;
					dislikes.textContent = parseInt(dislikes.textContent) + 1;
				}
			});
	}
	else if (!subs[post_id]['disliked']) {
		// Add a dislike
		var data = JSON.stringify({"post_id": post_id, "like": false, "dislike": true});
		$.post("/like",
			data,
			function(response){
				if (!response['status']) {
					alert('Something went wrong');
				}
				else {
					subs[post_id]['liked'] = false;
					subs[post_id]['disliked'] = true;
					$('#' + post_id + ' #dislike_button_small').first().toggleClass("disliked-small");
					var likes = $('#' + post_id + ' #likes')[0];
					var dislikes = $('#' + post_id + ' #dislikes')[0];
					dislikes.textContent = parseInt(dislikes.textContent) + 1;
				}
			});
	}
	else if (subs[post_id]['disliked']) {
		// Cancel the dislike
		var data = JSON.stringify({"post_id": post_id, "like": false, "dislike": false});
		$.post("/like",
			data,
			function(response){
				if (!response['status']) {
					alert('Something went wrong');
				}
				else {
					subs[post_id]['liked'] = false;
					subs[post_id]['disliked'] = false;
					$('#' + post_id + ' #dislike_button_small').first().toggleClass("disliked-small");
					var likes = $('#' + post_id + ' #likes')[0];
					var dislikes = $('#' + post_id + ' #dislikes')[0];
					dislikes.textContent = parseInt(dislikes.textContent) - 1;
				}
			});
	}
	else {
		alert('Something went wrong');
	}
}

function click_comment_small(post_id) {
	$('#' + post_id + ' #comment_button_small').first().toggleClass("showing-small");
	if ($('#' + post_id + ' #subcomments')[0].style.display === "none") {
		$('#' + post_id + ' #subcomments')[0].style.display = "block";
	} 
	else {
		$('#' + post_id + ' #subcomments')[0].style.display = "none";
	}
	$('#' + post_id + ' #subcomments blockquote').empty();
	get_subcomments(post_id);
}


function insert_subcomment(post_id, comment_id, commenter_id, commenter_name, time, content, likes, dislikes, comments, liked, disliked) {
	subs[comment_id] = {'type': 'comment', 'liked': liked, 'disliked': disliked, 'comments': comments};
	var date = new Date(time*1000);
	var time_string = ' ' +(date.getDay() + 1) + ', ' 
                  + monthNames[date.getMonth()] + ', '
                  + date.getFullYear();
	var new_comment = 
	`<div id="` + comment_id + `" class="excerpttxt">
		<ul class="nospace inline pushright font-xs">
			<li>
				<img src="/static/pictures/` + commenter_id + `" style="border-radius: 50%; height:18px;">
				</img>
			</li>
			<li>
				<ul class="nospace inline pushright font-xs">
					<li><h6 class="font-xxs">`+ commenter_name + `</h6></li>
					<ul class="nospace inline pushright"> 
						<li></i> <a class="font-xxs" href="/user=` + commenter_id + `">` + "@" + commenter_id + `</a></li>
						<li class="font-xxs"><i class="fa fa-calendar-o"></i>` + time_string + `</li>
					</ul>
				</ul>
			</li>
		</ul>
		<p class="font-xs">` + content + `</p>
		<ul class="nospace inline pushright font-xxs" style="margin-top: -20px;">
		  <li><button class="button button-like-small" id="like_button_small"  onclick="click_like_small(` + comment_id + `);">
				<i class="fa fa-heart"></i>
				<span id="likes">` + likes + `</span>
				</button> </li>
		  <li><button class="button button-dislike-small" id="dislike_button_small"  onclick="click_dislike_small(` + comment_id + `);">
				<i class="fa fa-thumbs-down"></i>
				<span id="dislikes">` + dislikes + `</span>
				</button> </li>
		  <li><button class="button button-comment-small" id="comment_button_small"  onclick="click_comment_small(` + comment_id + `);">
				<i class="fa fa-comment"></i>
				<span id="comments">` + comments + `</span>
				</button> </li>
		  <li><button class="button button-normal-small" onclick="click_reply_small(` + comment_id + `);">
				<i class="fa fa-pencil-square-o"></i>
				<span>Reply</span>
				</button> </li>
		  <li><button class="button button-normal-small">
				<i class="fa fa-share"></i>
				<span>Share</span>
				</button> </li>
		</ul>
		<div id='reply' style="padding-top: 0;padding-left: -2rem; display: none;">
			<textarea class="form-control" id="reply_text" rows="2" style:"font-size:.8rem;"></textarea>
			<button type="submit" class="btn btn-primary button-s" onclick="submit_subcomment(` + comment_id + `);">Submit</button>
		</div>
		<div id="subcomments" style="padding-top: 0;padding-left: -2rem; display:none;">
			<blockquote>
			</blockquote>
		</div>
		<div id='reply' style='display:none;'>
		</div>
	</div>`
	selector = $('#' + post_id + ' #subcomments blockquote')[0];
	selector.innerHTML += new_comment
	if (subs[comment_id]['liked']) {
		$('#' + comment_id + ' #like_button_small').toggleClass("liked-small");
	}
	if (subs[comment_id]['disliked']) {
		$('#' + comment_id + ' #dislike_button_small').toggleClass("disliked-small");
	}
	
}


function get_comments(post_id) {
	var data = JSON.stringify({"post_id":post_id,"time_stamp":0,"latest_comment_time_stamp":0});
	$.post("/get_comments",
		data,
		function(response){
			for (var i = 0; i < response.length; i++) {
				insert_comment(post_id, response[i].comment_id, response[i].commenter_id, response[i].commenter_name, response[i].time, 
					response[i].content, response[i].likes, response[i].dislikes, response[i].comments, response[i].liked, response[i].disliked);
			}
	});
}

function get_subcomments(comment_id) {
	var data = JSON.stringify({"post_id":comment_id,"time_stamp":0,"latest_comment_time_stamp":0});
	$.post("/get_comments",
		data,
		function(response){
			for (var i = 0; i < response.length; i++) {
				insert_subcomment(comment_id, response[i].comment_id, response[i].commenter_id, response[i].commenter_name, response[i].time, 
					response[i].content, response[i].likes, response[i].dislikes, response[i].comments, response[i].liked, response[i].disliked);
			}
	});
}

function select_tag(index) {
	$('#rightbar aside div ul li .nav-link').removeClass('active');
	var selector = $('#rightbar aside div ul li #tab'+index).addClass('active');
	$('#rightbar .tab_selection').css('display', 'none');
	$('#rightbar #selection' + index).css('display', 'block');
}
 
function submit_post() {
	var content = $('#rightbar #post_text').val();
	var time = Date.now() / 1000;
	var data = JSON.stringify({
		"time_stamp": time, 
		"content": content,
		"visibility": "public"
	});
	$.post("/post",
		data,
		function(response){
			if (response['status']) {
				prepend_post(response.id, self_id, self_name, time, 
					content, 0, 0, 0, false, false);
				$('#rightbar #post_text').val("");
			}
	});
}