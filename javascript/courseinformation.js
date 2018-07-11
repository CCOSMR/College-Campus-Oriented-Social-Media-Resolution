
            function request_comment() {
                var c = document.getElementById("comment").value;
                var data = JSON.stringify({"comment":c});
                $.post("/submitcomment",
                    data,
                    function(n){
                            alert(data);
                            alert(n);
                        }                   
                    );
            }            
