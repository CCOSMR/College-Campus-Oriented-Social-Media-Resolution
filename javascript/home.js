var time_stamp = Date.now();
var earliest_post_id = -1;
var post_count = 0;
var post_ids = [];
var liked = [];
var disliked = [];

const monthNames = ["January", "February", "March", "April", "May", "June",
  "July", "August", "September", "October", "November", "December"
];


$(function() {
	$('.button-like').on('click', function () {
		$(this).toggleClass("liked");
	});
});

jQuery(function($) {
	jQuery(window).scroll(function(){
	 var ScrollTop = jQuery(window).scrollTop();
	 var data;
	 var data = JSON.stringify({"time_stamp":time_stamp,"type":"backward"});
	 
	 if ($(this).scrollTop() + $(window).innerHeight() + 1 >= $("#content-wrapper").innerHeight()) { 
		
	  $.post("/request_posts",
			data,
			function(response){
				for (var i = 0; i < response.length; i++) {
					insert_post(response[i].poster_id, response[i].poster_name, response[i].time, 
						response[i].content, response[i].likes, response[i].dislikes, response[i].comments);
				}
			});
	 }
	 });
	 
	 time_stamp = Date.now();
});

function check_post() {
	 var ScrollTop = jQuery(window).scrollTop();
	 var data;
	 var data = JSON.stringify({"time_stamp":time_stamp,"type":"backward"});
	 
	 if ($(this).scrollTop() + $(window).innerHeight() + 1 >= $("#content-wrapper").innerHeight()) { 
		
	  $.post("/request_posts",
			data,
			function(response){
				for (var i = 0; i < response.length; i++) {
					insert_post(response[i].poster_id, response[i].poster_name, response[i].time, 
						response[i].content, response[i].likes, response[i].dislikes, response[i].comments);
					post_ids.push(response[i].post_id);
				}
			});
	 }
	 
	 
	 time_stamp = Date.now();
}

function insert_post(poster_id, poster_name, time, content, likes, dislikes, comments) {
	post_count++;
	var date = new Date(time*1000);
	var time_string = ' ' +(date.getDay() + 1) + ', ' 
                  + monthNames[date.getMonth()] + ', '
                  + date.getFullYear();
	new_post = `<li id="post` + post_count + `"><article class="excerpt">
								<div class="excerpttxt">
									
							
									<ul class="nospace inline pushright font-xs">
										<li>
											<ul class="nospace inline pushright font-xs">
												<li><h6 class="heading">`+ poster_name + `</h6></li>
												<ul class="nospace inline pushright font-xs"> 
													<li></i> <a href="#">` + "@" + poster_id + `</a></li>
													<li><i class="fa fa-calendar-o"></i>` + time_string + `</li>
												</ul>
											</ul>
										</li>
									</ul>
									<p>` + content + `</p>
									
									<ul class="nospace inline pushright font-xs">
									  <li><button class="button button-like" id="like_button_` + post_count + `">
											<i class="fa fa-heart"></i>
											<span>` + likes + `</span>
											</button> </li>
									  <li><button class="button button-dislike" id="dislike_button_` + post_count + `">
											<i class="fa fa-thumbs-down"></i>
											<span>` + dislikes + `</span>
											</button> </li>
									  <li><button class="button button-normal">
											<i class="fa fa-comment"></i>
											<span>` + comments + `</span>
											</button> </li>
									  <li><button class="button button-normal">
											<i class="fa fa-pencil-square-o"></i>
											<span>Reply</span>
											</button> </li>
									  <li><button class="button button-normal">
											<i class="fa fa-share"></i>
											<span>Share</span>
											</button> </li>
									</ul>
								</div>
							</article></li>  `
	
	liked.push(false);
	disliked.push(false);
	
	document.getElementById('posts_list').innerHTML += new_post;
	$(function() {
		$('.button-like').on('click', function () {
			var index = parseInt($(this).attr('id').slice(12));
			if(disliked[index - 1]) {
				$('#dislike_button_' + index.toString()).toggleClass("disliked");
				disliked[index - 1] = false;
			}
			liked[index - 1] = !liked[index - 1];
			$(this).toggleClass("liked");
			
		});
	});
	$(function() {
		$('.button-dislike').on('click', function () {
			var index = parseInt($(this).attr('id').slice(15));
			if(liked[index - 1]) {
				$('#like_button_' + index.toString()).toggleClass("liked");
				liked[index - 1] = false;
			}
			disliked[index - 1] = !disliked[index - 1];
			$(this).toggleClass("disliked");

		});
	});
}

function select_tag(index) {
    var i;
    var x = document.getElementsByClassName("tab_selection");
    for (i = 0; i < x.length; i++) {
        x[i].style.display = "none"; 
    }
    document.getElementsByClassName('tab_selection')[index].style.display = "block"; 
	
	var y = document.getElementsByName('tab');
	for (i = 0; i < y.length; i++) {
        y[i].className = "nav-link"
    }
	document.getElementsByName('tab')[(y.length - 1) % (index + 1)].className = "nav-link active"; 
}

