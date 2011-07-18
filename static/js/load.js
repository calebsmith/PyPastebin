//Basic AJAX from W3Schools
/*
var xmlhttp;
function loadXMLDoc(url,cfunc){
    if (window.XMLHttpRequest){
        xmlhttp=new XMLHttpRequest();
    }
    else{
        xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
    }
    xmlhttp.onreadystatechange=cfunc;
    xmlhttp.open("GET",url,true);
    xmlhttp.send();
}
function myFunction(){
    loadXMLDoc("../images/wood.jpeg",function(){
        if (xmlhttp.readyState==4 && xmlhttp.status==200){
            document.getElementById("myDiv").innerHTML=xmlhttp.responseText;
        }
  });
}
*/

//toggle divs on/off and fade them
var div_toggler = function(){
    id_map = ['detail_loading']
    id_stat = [];
    for (var i = 0; i < id_map.length; i++){
        id_stat.push('0');
    }
        toggle = function(value_in){
            if(id_stat[value_in] == 0) {
                $("#"+id_map[value_in]).fadeIn("slow");
                id_stat[value_in] = 1;
                return toggle;
            }
            if (id_stat[value_in] == 1) {
                $("#" + id_map[value_in]).fadeOut("slow");
                id_stat[value_in] = 0;
            }
        };
        hide_all = function(){
            for(var i = 0; i < id_map.length; i++){
                id_stat[i] = 0
                $("#"+id_map[i]).hide();
            }
        };
    return {
        'toggle' : toggle,
        'hide_all' : hide_all
    };
}();

//for swapping among divs in a list
var div_swapper = function() {
    var div_current = -1,
    id_map = ['detail_tabs','detail_loading'],
    all_id_map = "#" + id_map.join(", #");        
    
        hide_all = function(){
        	$(all_id_map).hide();
        },
        
        show = function(value_in){
            if (value_in != div_current){            
                $("#"+id_map[div_current]).hide();
                div_current = value_in;
                $("#"+id_map[value_in]).fadeIn("slow");
            }
        };             

    return {
        'show': show,
        'hide_all' : hide_all
    };
}();

$(document).ready(function(){

});
