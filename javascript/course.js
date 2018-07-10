
            function request_searchcourse() {
                var searchname = document.getElementById("mysearch").value;
                alert(searchname);
                var data = JSON.stringify({"search":searchname});
                $.post("/course",
                    data,
                    function(n){
                        alert("6666666");
                        /*var box = document.getElementById("resulttable");
                        for(var i=0;i<n.length;i++){
                            var str1=`
                                                        <tr>
                                                            <td><h5>`+`</h5></td>
                                                            <td<h5>`+`</h5></td>
                                                            <td><h5>`+`</h5></td>
                                                            <td><h5>`+`</h5></td>
                                                        </tr> 
                            `;
                            box.innerHTML +=str1;    
                        } */                    
                    });
            }
            
            function show(){
                request_searchcourse();
            }

            function getRadioGrade(a){
                var data = JSON.stringify({"grade":a});
                $.post("/searchgrade",
                    data,
                    function(){
                    });
            }

            function getRadioClasstype(a){
                var data = JSON.stringify({"classtype":a});
                $.post("/searchclasstype",
                    data,
                    function(){
                    });
            }

            function abc(){
                $.post("/test",
                    function(b){
                        alert(b);
                    });
            }

            function efg(){
                var box = document.getElementById("resulttable");
                var str="dadasdsadasd"
                var str1=`
                                            <tr>
                                                <td>`+str+`</td>
                                                <td>Rachel Johnson</td>
                                                <td>19</td>
                                                <td>60</td>
                                            </tr> 
                `;
                box.innerHTML +=str1;
            }
 