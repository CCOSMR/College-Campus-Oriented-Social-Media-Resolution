
 function getCurrentTime(){
   	   var today=new Date();
   	   var y=today.getFullYear();
   	   var mh=today.getMonth();
   	   mh++;
   	   var d=today.getDate();
   	   var h=today.getHours();
   	   var m=today.getMinutes();
   	   var s=today.getSeconds();
   	   m=checkTime(m)
       s=checkTime(s)
       var time=y+"-"+mh+"-"+d+"  "+h+":"+m+":"+s;
       return time;
   }
   function checkTime(i){
       if(i<10)
         i="0"+i
       return i
    }
