#include <stdio.h>
#include <stdlib.h>
#include <iostream>
#include <string.h>
#include "slist.h"

/*String_list includes the following public methods
clear()				-clear the list
make(int n)			-make n strings in memory
assign(int m, string n)		-at point m, overwrite with string n. Must be allocated with make() first.
>> string n 			-for output(drops the last string in list)
<< string n			-add n to the end of the list
=				-make a String_list object equivalent to another.
swap (int x, int y)		-swap the strings in place x and place y
int n = length()		-return n as length of a String_list
parse(string n)			-clear the list and parse n into several strings. Put them in the list
parse(string n, string key)	-same as above but using a delimiter other than " "
parselength(string n)		-what would the size of the list be if n were parsed
string n = combine()		-combine the list into string n
push(string n)			-same as <<
remove(int n)			-remove string in place n from the list			
insert(int m, string n)		-at point m, insert string n
string n = view	(int m)		-return n for the string at m in the list

*/
int main(int argc, char* argv[])
{
	String_list svect;
	
	string out;
	while(1){
		cout << '\n' << "Enter some text and I will parse it for you." << '\n';
		getline(cin, out);
		svect.parse(out);
		//check for quitting
		if (out.compare("/quit") == 0 || out.compare("/exit") == 0) return 1;
		//list result
		svect.list();
		
	    cout << '\n';
	}
	return 1;
}
