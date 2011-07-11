#include <iostream>
#include <fstream>
#include <sstream>
#include <string.h>

#include "setclass.h"
#include "slist.h"
#include "settings.h"

#include "constants.h"
#include "functions.h"
using namespace std;

bool script_handler(Program_settings& settings, String_list& input, Page& setclass){
  
    String_list buffer, var_list;
    bool load_success;   
    string filename;
    input >> filename; 
    
    //load script into memory, return if file fails to open. 
    //load variable names into var_list
    load_success = load_script_file(filename, buffer, var_list);    
    if (load_success == 0) return 0;
    
    int i, i2, i3;
    int vars;
    vars = var_list.length();
    
    //assign memory for variables
    int* var_value;
    string* var_name;
    var_value = new int[vars + 1];
    var_name = new string[vars + 1];
    
    //assign variable names obtained from var_list
    for(i = 0; i < vars; i++){
        var_list >> var_name[i]; 
    }
    //run the script
    int file_length = buffer.length();
    string line;
    String_list proc_line;
    string name_in;
    string str_val_in;
    int value_in;
    int global_val;
    bool isanumber, isaglobal;
    for(i = 0; i < file_length; i++){
        line = buffer.get(i);       //obtain the next line
        if (line == "end") break;   //exit if script command is "end"         
        proc_line.parse(line);      //parse the current line
        
        //show line if echo on
        if (settings.get_echo() == 1) cout << line << '\n'; 
        
        //assign variables
        if (proc_line.get(1) == "="){
            isanumber = 1;
            isaglobal = 0;
            name_in = proc_line.get(0);
            str_val_in = proc_line.get(2);
            value_in = string_to_int(str_val_in);
            //detect if assignment is var to number of var to var
            if (value_in == 0 && str_val_in != "0") isanumber = 0;
            
            for(i2 = 0; i2 < vars; i2++){
                if (name_in == var_name[i2]){
                    //if assigning a variable to a number
                    if (isanumber == 1){
                        var_value[i2] = value_in;
                        break;
                    }
                    
                    //if assigning a variable to another variable
                    if (isanumber == 0){
                        //check for globals
                        for(i3 = 0; i3 < settings.globals.length(); i3++){                        
                            if (str_val_in == settings.globals.get(i3)){
                                isaglobal = 1;   
                                global_val = find_global(settings.globals.get(i3), setclass);
                                var_value[i2] = global_val;
                                break;
                            }
                        }
                        if (isaglobal == 1) continue;
                        
                        //not a global, check for local variables                        
                        for(i3 = 0; i3 < vars; i3++){                            
                            if (str_val_in == var_name[i3]){
                                var_value[i2] = var_value[i3];
                                break;
                             }
                        }                        
                    }
                    cout << var_name[i2] << " is now = to " << var_value[i2] << '\n';
                    break;
                }
            }
            
            continue;
        }
        
        //reaching this point means the line contains a regular command.
        //execute that command    
        command_handler(settings, proc_line, setclass);
    }
        
    return 1;
}
bool load_script_file(string filename, String_list& buffer, String_list& var_list){
    //convert filename to char* for opening the file
    char name [255] = "";
    stringstream scr_fn;
    scr_fn << filename;
    strcat (name, scr_fn.str().c_str());
    
    fstream fin;
    fin.open(name, ios_base::in);
        //attempt to open the file and report failure
        if (fin.fail()) {cout << "Failed to load script: " << filename << '\n'; return 0;}
               
       
        //load file into a buffer and count the number of variables
        int vars = 0;
        bool samename;
        String_list proc_line;
        string line, name_in;
        int i;
        while(fin.eof() != 1){
            getline(fin, line);     //obtain a line from the file
            buffer << line;         //store in buffer
            proc_line.parse(line);  //parse the line for processing
            
            //line added to buffer, now check for variable assignments
            if (proc_line.length() > 1){
                if (proc_line.get(1) == "="){
                    name_in = proc_line.get(0);
                    //check that the variable name is unique
                    samename = 0;
                    for(i = 0; i < vars; i++){                    
                        if (var_list.get(i) == name_in){
                            samename = 1;
                        }                          
                    }
                    //if the variable is unique, add the name to the list
                    if (samename == 0){
                        var_list << name_in;
                        vars++;
                    }
                }
            }
            if(line == "end") break;
        }
    fin.close();
    return 1;
}
int string_to_int(string str_in){
    stringstream val;
    int int_out;       
    
    val << str_in;
    val >> int_out;    
    return int_out;
}
int find_global(string global_name, Page& setclass){
    int value;    
    if(global_name == "TABS"){ value = setclass.get_tab_size(); return value;}
    if(global_name == "TAB"){ value = setclass.get_tab_number();return value;}
    if(global_name == "SETS"){ value = setclass.get_size(); return value;}
    if(global_name == "SET"){  value = setclass.get_iter(); return value;}
    
    
    if(global_name == "SETINT"){value =  setclass.get_integer(); return value;}       
    if(global_name == "SCINT") {value =  setclass.get_sc_integer(); return value;}        
    if(global_name == "SETBIN") {}
    if(global_name == "SCBIN") {}
    
    if(global_name == "INPUT"){value =  setclass.get_integer(); return value;}
    if(global_name == "SC") { value =  setclass.get_sc_integer(); return value;}
    
    //if(global_name == "FNAME"){  get_fname(); return value;}
    //if(global_name == "ICV") { get_icv(); return value;}

    if(global_name == "COMPLIMENT"){value = setclass.get_compliment(); return value;}
    if(global_name == "MPARTNER"){value = setclass.get_mpartner(); return value;}
    if(global_name == "ZPARTNER") {value = setclass.get_zpartner(); return value;}
    /*
    if(global_name == "INPUT")  list_string(get_integer()) << '\n'; return value;}
    if(global_name == "SC") {  list_string(get_sc_integer(), 2) << '\n'; return value;}
    if(global_name == "FNAME"){  get_fname() << '\n'; return value;}
    if(global_name == "ICV") { list_string(get_icv(),3) << '\n'; return value;}

    if(global_name == "COMPLIMENT"){list_string(get_compliment(),2) <<'\n'; return value;}
    if(global_name == "MPARTNER"){list_string(get_mpartner(),2) << '\n'; return value;}
    if(global_name == "ZPARTNER") {list_string(get_zpartner(),2); return value;}
    */     
    return 0;
}
