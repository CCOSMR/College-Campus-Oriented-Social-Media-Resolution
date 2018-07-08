var last_refresh_time = Date.now();
var earliest_post_id = -1;
var post_count = 0;
var post_ids = [];

jQuery(function($) {
	jQuery(window).scroll(function(){
	 var ScrollTop = jQuery(window).scrollTop();
	 var data;
	 var data = JSON.stringify({"last_refresh_time":last_refresh_time,"earliest_post_id":earliest_post_id});
	 
	 if ($(this).scrollTop() + $(window).innerHeight() + 1 >= $("#content-wrapper").innerHeight()) { 
	  alert("Load data");
	  alert(Date.now());
	  insert_post(1, 1, 1, 1, 1, 1, 1);
	  $.post("/request_posts",
			data,
			function(){
				
			});
	 }
	 });
	 
	 last_refresh_time = Date.now();
});


function insert_post(poster_id, poster_display_name, time, content, likes, dislikes, comments) {
	new_post = `<article class="excerpt">
								<div class="excerpttxt">
									
							
									<ul class="nospace inline pushright font-xs">
										<li>
											<ul class="nospace inline pushright font-xs">
												<li><h6 class="heading">Posuere lorem placerat</h6></li>
												<ul class="nospace inline pushright font-xs">
													<li><i class="fa fa-comments"></i> <a href="#">@user_id</a></li>
													<li><i class="fa fa-calendar-o"></i> 02/01/45</li>
												</ul>
											</ul>
										</li>
									</ul>
									<p>Nunc non erat molestie faucibus duis aliquam rutrum sapien non pretium tortor lacinia auctor donec et ullamcorper lacus&hellip;</p>
									
									<ul class="nospace inline pushright font-xs">
									  <li><i class="fa fa-calendar-o"></i> 02/01/45</li>
									  <li><i class="fa fa-comments"></i> <a href="#">4</a></li>
									  <li><i class="fa fa-eye"></i> 10</li>
									</ul>
								</div>
							</article>  `
												
	document.getElementById('posts_list').innerHTML += new_post;
}
