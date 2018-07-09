var id_regex = /^\w{3,24}$/i
var name_regex = /^[\u0000-\uD7AF\uF900-\uFAFF]{1,24}$/u
var password_regex = /^(\w|@|#|\$|\^|&|\(|\)|-|\+|=|!|`|~|\{|\}|\[|\]|\\|\:|\;|\'|\"|\<|\>|\,|\.|\?|\/|%|\*|\s){6,24}$/i
var warning_password_regex = /@|#|\$|\^|&|\(|\)\+|=|!|`|~|\{|\}|\[|\]|\\|\:|\;|\'|\"|\<|\>|\,|\.|\?|\/|%|\*|\s/g
var email_regex = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/

var captcha_regex = /^[a-zA-Z0-9]{3,24}$/i


	
function fetch_captcha() {
	var scroll = $(window).scrollTop();
	var d=new Date();
	document.getElementById("captcha_image").innerHTML = "<image class='captcha_image' style='vertical-align:middle' src='/captcha?height=220&width=100&time="+d.getTime()+"'>";	
	$("html").scrollTop(scroll);
	document.querySelector('.captcha_image').addEventListener('click', function() {
	  var d=new Date();
	  var ran = d.getTime();
	  this.setAttribute('src', '/captcha?height=220&width=100&time='+ran);
	});
	return false;
}



function request_signup() {
	var id = document.getElementById("id").value;
	var password = document.getElementById("password").value;
	var name = document.getElementById("name").value;
	var email = document.getElementById("email").value;
	var captcha = document.getElementById("captcha").value;
	var data = JSON.stringify({"id":id,"password":password,"email":email,"name":name,"captcha":captcha});
	$.post("/register",
		data,
		function(datar){
			if(datar.status== true)
				{window.location = datar.url;}
			else  
            {
                alert("register failed");
                window.location = datar.url;
            }	
		},
		dataType = "json"
		);
}

function enter_id() {

	if (document.getElementById('id').value.length < 1) {
		document.getElementById('id_message').innerHTML = "<div class='alert alert-danger' role='alert'>You need to set an ID</div>";
		return false;
	}
	else if (document.getElementById('id').value.length < 3) {
		document.getElementById('id_message').innerHTML = "<div class='alert alert-danger' role='alert'>Your ID needs to be at lease 3 digits long</div>";
		return false;
	}
	else if (document.getElementById('id').value.length > 24) {
		document.getElementById('id_message').innerHTML = "<div class='alert alert-danger' role='alert'>Your ID needs to be no more than 24 digits long</div>";
		return false;
	}
	else if (id_regex.test(document.getElementById('id').value)==false) {
		document.getElementById('id_message').innerHTML = "<div class='alert alert-danger' role='alert'>ID can only contain letters, numbers or underscores</div>";
		return false;
	}
	else {
		document.getElementById('id_message').innerHTML = "";
		return true;
	}
}

function enter_name() {
	if (document.getElementById('name').value.length < 1) {
		document.getElementById('name_message').innerHTML = "<div class='alert alert-danger' role='alert'>Your have to enter a display name</div>";
		return false;
	}
	else if (document.getElementById('name').value.length > 24) {
		document.getElementById('name_message').innerHTML = "<div class='alert alert-danger' role='alert'>Your display name needs to be no more than 24 digits long</div>";
		return false;
	}
	else if (name_regex.test(document.getElementById('name').value)==false) {
		document.getElementById('name_message').innerHTML = "<div class='alert alert-danger' role='alert'>Unsupported charactors, must be Unicode 0000 - D7AF</div>";
		return false;
	}
	else {
		document.getElementById('name_message').innerHTML = "";
		return true;
	}
}

function enter_password() {
	check_password();
	if (document.getElementById('password').value.length < 1) {
		document.getElementById('password_message').innerHTML = "<div class='alert alert-danger' role='alert'>You need to set a password</div>";
		return false;
	}
	else if (document.getElementById('password').value.length < 6) {
		document.getElementById('password_message').innerHTML = "<div class='alert alert-danger' role='alert'>Password needs to be at lease 6 digits long</div>";
		return false;
	}
	else if (document.getElementById('password').value.length > 24) {
		document.getElementById('password_message').innerHTML = "<div class='alert alert-danger' role='alert'>Password needs to be no more than 24 digits long</div>";
		return false;
	}
	else if (password_regex.test(document.getElementById('password').value)==false) {
		document.getElementById('password_message').innerHTML = "<div class='alert alert-danger' role='alert'>Password can only contain letters, numbers, spaces or charactors on a standard keyboard</div>";
		return false;
	}
	else if (warning_password_regex.test(document.getElementById('password').value)) {
		document.getElementById('password_message').innerHTML = "<div class='alert alert-warning' role='alert'>Unusual charactors detected. Please make sure you can remember this password.</div>";
		return true;
	}
	else {
		document.getElementById('password_message').innerHTML = "";
		return true;
	}
}

function check_password() {
	if (document.getElementById('password').value ==
		document.getElementById('confirm_password').value) {
			document.getElementById('confirm_message').innerHTML = "<div class='alert alert-success' role='alert'>Your passwords matched</div>";
			return true;
	} else {
		document.getElementById('confirm_message').innerHTML = "<div class='alert alert-danger' role='alert'>Your passwords don't match</div>";
		return false;
	}
}

function enter_email() {
	if (document.getElementById('email').value.length < 1) {
		document.getElementById('email_message').innerHTML = "<div class='alert alert-danger' role='alert'>You need to enter an email</div>";
		return false;
	}
	else if (email_regex.test(document.getElementById('email').value)==false) {
		document.getElementById('email_message').innerHTML = "<div class='alert alert-danger' role='alert'>You have to enter a valid email</div>";
		return false;
	}
	else {
		document.getElementById('email_message').innerHTML = "";
		return true;
	}
}

function enter_captcha() {
	if (document.getElementById('captcha').value.length != 4) {
		document.getElementById('captcha_message').innerHTML = "<div class='alert alert-danger' role='alert'>Captcha is 4-digits long</div>";
		return false;
	}
	else if (captcha_regex.test(document.getElementById('captcha').value)==false) {
		document.getElementById('captcha_message').innerHTML = "<div class='alert alert-danger' role='alert'>Captcha only contains letters and numbers</div>";
		return false;
	}
	else {
		document.getElementById('captcha_message').innerHTML = "";
		return true;
	}
}

function check_form() {
	if (enter_id() == true && enter_name()== true && enter_password() == true && check_password () == true && enter_email() == true && enter_captcha() == true) {
		request_signup();
	}
	else {
		alert("Please complete the form.");
	}
}
