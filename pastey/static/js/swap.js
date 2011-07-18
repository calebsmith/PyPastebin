//for selecting among divs and swapping one for the other
var option_button = function() {
    var win_current = -1,
    id_map = ['Gnome', 'KDE', 'XFCE', 'Openbox', "debian", "redhat", "slackware", 
    		"gentoo", "suse", "fedora", "puppy", "ubuntu"],
    all_id_map = "#" + id_map.join(", #");
        
        hide_all = function(){
        	$(all_id_map).hide();
        },
        win_show = function(value_in) {
            if (value_in != win_current) {
            
                $("#"+id_map[win_current]).hide();
                win_current = value_in;
                $("#"+id_map[value_in]).fadeIn("slow");
            }
        };             

    return {
        'win_show': win_show,
        'hide_all' : hide_all
    };
}();
//for toggling divs on and off
var toggle_button = function() {
	//map divs to numbers
	id_map = ['synaptic','deb_rpm', 'apt-get', 'tar', 'source'],
	//establish a bool for each div holding its display status (0=hidden)
	id_stat = [];
	for (var i = 0; i < id_map.length; i++){
		id_stat.push('0');
	}	
	//toggling function that will fade in/out according to id_stat value
		toggle = function(value_in){
			if (id_stat[value_in] == 0)	{
				$("#"+id_map[value_in]).fadeIn("slow");	
				id_stat[value_in] = 1;			
				return toggle;								
			}
			if (id_stat[value_in] == 1)	{
				$("#"+id_map[value_in]).hide();
				id_stat[value_in] = 0;
			}
		};
	//function that will toggle all divs to 0 and hide them
		hide_all = function(){
			for(var i = 0; i < id_map.length; i++){
				id_stat[i] = 0;
				$("#"+id_map[i]).hide();
			}
		};
	return {
		'toggle' : toggle,
		'hide_all' : hide_all
	};	
}();

$(document).ready(function(){
	//option_button.hide_all();
	
});

