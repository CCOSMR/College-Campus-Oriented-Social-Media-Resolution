 var id="";


 

 function fillinfo(){
                insert_userid(id);
                $.get("/personalinfo"?id,
                    function(info){
                      
                      insert_username(info["person".name]);
                      insert_useremail(info["person".email]);

                      for(var i=0;i<info["courses"].length;i++)
                      {
                        insert_coursename(info["courses"][i]);
                      }

                      for(var j=0;i<info["friends"].length;j++)
                      {
                        insert_friendname(info["courses"][j]);
                      }
                    });
        }


function insert_userid() {
    var id="123"
    var str0="<span class="text-left" style='color: #ffffff;'>"+id+"</span>";

    document.getElementById('userid').innerHTML = str0;
  }


  function insert_username(username) {
    var str1="<span class="text-left" style='color: #ffffff;'>"+username+"</span>";

    document.getElementById('username').innerHTML = str1;
  }



   function insert_useremail(useremail) {

   var str2="<span class="text-left" style='color: #ffffff;'>"+useremail+"</span>";

    document.getElementById('username').innerHTML = str2;
  }



    function insert_coursename(coursename) {

   var str3=" <li class="nav-item"><a class="nav-link" href="">"+coursename+"</a></li>";

    document.getElementById('MenuDropdown').innerHTML = str3;
  }



    function insert_friendname(friendname) {

   var str4=" <li class="nav-item"><a class="nav-link" style="background-color: #cbecf1;">"+friendname+"</a></li>";

    document.getElementById('MenuDropdown1').innerHTML = str4;
  }


        
   
     

