var id_regex = /^\w{3,24}$/i
	var name_regex = /^[\u0000-\uD7AF\uF900-\uFAFF]{1,24}$/u
	var password_regex = /^(\w|@|#|\$|\^|&|\(|\)|-|\+|=|!|`|~|\{|\}|\[|\]|\\|\:|\;|\'|\"|\<|\>|\,|\.|\?|\/|%|\*|\s){6,24}$/i
	
	
	function request_login() {
		var id = document.getElementById("id").value;
		var password = document.getElementById("password").value;
		var data = JSON.stringify({"id":id,"password":password,"captcha":""});
		
		$.post("/login",
			data,
			function(response){
				
				if(response.status==false) {
					document.getElementById('message').innerHTML = 
						"<div class='alert alert-danger' role='alert'>Username and password does not match.</div>";
				}
				else {
					window.location.href = '/home';
				}
			});
	}
	
	function enter_id() {
	
		if (document.getElementById('id').value.length < 1) {
			document.getElementById('message').innerHTML = "<div class='alert alert-danger' role='alert'>Enter user ID and password</div>";
			return false;
		}
		else if (document.getElementById('id').value.length < 3) {
			document.getElementById('message').innerHTML = "<div class='alert alert-danger' role='alert'>Invalid user ID or password format</div>";
			return false;
		}
		else if (document.getElementById('id').value.length > 24) {
			document.getElementById('message').innerHTML = "<div class='alert alert-danger' role='alert'>Invalid user ID or password format</div>";
			return false;
		}
		else if (id_regex.test(document.getElementById('id').value)==false) {
			document.getElementById('message').innerHTML = "<div class='alert alert-danger' role='alert'>Invalid user ID or password format</div>";
			return false;
		}
		else {
			document.getElementById('message').innerHTML = "";
			return true;
		}
	}
	
	function enter_password() {
		if (document.getElementById('password').value.length < 1) {
			document.getElementById('message').innerHTML = "<div class='alert alert-danger' role='alert'>Enter user ID and password</div>";
			return false;
		}
		else if (document.getElementById('password').value.length < 6) {
			document.getElementById('message').innerHTML = "<div class='alert alert-danger' role='alert'>Invalid user ID or password format</div>";
			return false;
		}
		else if (document.getElementById('password').value.length > 24) {
			document.getElementById('message').innerHTML = "<div class='alert alert-danger' role='alert'>Invalid user ID or password format</div>";
			return false;
		}
		else if (password_regex.test(document.getElementById('password').value)==false) {
			document.getElementById('message').innerHTML = "<div class='alert alert-danger' role='alert'>Invalid user ID or password format</div>";
			return false;
		}
		else {
			document.getElementById('message').innerHTML = "";
			return true;
		}
	}
	
	function check_form() {
		if (enter_id() && enter_password()) {
			request_login();
		}
	}