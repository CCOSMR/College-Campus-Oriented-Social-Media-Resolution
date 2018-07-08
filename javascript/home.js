var time_stamp = Date.now();
var earliest_post_id = -1;
var post_count = 0;
var post_ids = [];
const monthNames = ["January", "February", "March", "April", "May", "June",
  "July", "August", "September", "October", "November", "December"
];

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


function insert_post(poster_id, poster_name, time, content, likes, dislikes, comments) {
	var date = new Date(time);
	var time_string = date.getDay() + ', ' 
                  + monthNames[date.getMonth()] + ', '
                  + date.getFullYear();
	new_post = `<article class="excerpt">
								<div class="excerpttxt">
									
							
									<ul class="nospace inline pushright font-xs">
										<li>
											<ul class="nospace inline pushright font-xs">
												<li><h6 class="heading">`+ poster_name + `</h6></li>
												<ul class="nospace inline pushright font-xs">
													<li><i class="fa fa-comments"></i> <a href="#">` + poster_id + `</a></li>
													<li><i class="fa fa-calendar-o"></i>` + time_string + `</li>
												</ul>
											</ul>
										</li>
									</ul>
									<p>` + content + `</p>
									
									<ul class="nospace inline pushright font-xs">
									  <li><i class="fa fa-calendar-o"></i>` + likes + `</li>
									  <li><i class="fa fa-comments"></i>` + dislikes + `</li>
									  <li><i class="fa fa-eye"></i>` + comments + `</li>
									</ul>
								</div>
							</article>  `
	
	document.getElementById('posts_list').innerHTML += new_post;
}
