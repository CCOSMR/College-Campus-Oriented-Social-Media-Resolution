
            function request_searchcourse() {
                var searchname = document.getElementById("mysearch").value;
                var data = JSON.stringify({"search":searchname});
                $.post("/course",
                    data,
                    function(n){
                        var box = document.getElementById("resulttable");
                        box.innerHTML=`
                                            <tr>
                                                <th>ID</th>
                                                <th>Name</th>
                                                <th>Score</th>
                                                <th>Course number</th>
                                            </tr>                        
                        `
                        for(var i=0;i<n.length;i++){
                            var str1=`
                                                        <tr>
                                                            <td><h5>`+n[i].id+`</h5></td>
                                                            <td><h5>`+` <a href="course?courseid=`+n[i].id+`">`+n[i].name+`</a>`+`</h5></td>
                                                            <td><h5>`+n[i].ave_rating+`</h5></td>
                                                            <td><h5>`+60+`</h5></td>
                                                        </tr>                                
                            `;
                            box.innerHTML +=str1;    
                        }           
                    });
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
                var str="链接测试";
                var str1=`
                                            <tr>
                                                <td>`+` <a href="course?courseid=1">`+str+`</a>`+`</td>
                                                <td>Rachel Johnson</td>
                                                <td>19</td>
                                                <td>60</td>
                                            </tr> 
                `;
                box.innerHTML +=str1;
            }
 