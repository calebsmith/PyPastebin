//CSRF for Django >=1.2 and JQuery>=1.5.1
$(document).ajaxSend(function(event, xhr, settings) {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    function sameOrigin(url) {
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }
    function safeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }
});

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

    $('select').attr('onchange',"this.form.submit()");

   // $.get('', function(response) {if (response == 1){div_toggler.toggle(0);}});
});
