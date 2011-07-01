using namespace std;
//using namespace std;

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


class String_list{
	private:
		string *a;
		int size;
	public:
		String_list(){
			a = new string[1];	
			size = 0;	
		}	
		String_list(string in){
		    String_list();
		    parse(in);
		}
		~String_list(){
			delete [] a;
		}
		String_list& operator=(const String_list &in){
			if (&in == this) return *this;	
			int i;
			size = in.size;
			delete [] a;
			a = new string[size];
			for (i = 0; i < size; i++){a[i] = in.a[i];}	
			return *this;	
		}
		
		void operator << (string in){push(in); return;}
		string operator >> (string &out){out = pop(); return out;}
		
		string pop (){
		    string out = " ";
		    if (size < 0) return out;
		    out = view(size - 1);
		    remove(size - 1);
		    return out;
		}
		string lpop(){
		    string out = " ";
		    //if (size < 1) return out;
		    out = view(0);
		    remove(0);
		    return out;
		}
		void swap(int x, int y){
			if (x >= size || y >= size || x < 0 || y < 0) return;
			string strx, stry,strz;
			strx = a[x];
			stry = a[y];
			strz = strx;
			strx = stry;
			stry = strz;
			a[x] = strx;
			a[y] = stry;
			return;
		}
		int parselength(string in){
			int answer = 0;
			string send = "";
			string check = "";
			int length = in.length();
			int i;
			for (i = 0; i < length; i++)
			{			
				send += in[i];
				check.clear();
				check += in[i];
				if (check.compare(" ") == 0 || i == (length - 1))
				{
					answer++;
				}
				
			}	
			return answer;
		}
		void parse(string in){
			string key = " ";
			parse(in,key);
			return;
		}
		void parse(string in, string key){	
			int i;
			string send = "";
			string check = "";
			int length = in.length();
			int sendlength;
			clear();
			for (i = 0; i < length; i++)
			{			
				send += in[i];
				check.clear();
				check += in[i];
				if (check.compare(key) == 0 || i == (length - 1))
				{
					sendlength = send.length();
					if (i < (length - 1))send.erase(sendlength - 1);//drop last character, which is the delimiter				
					
					if (send.compare(key) != 0 && send.length() > 0) push(send);//if not the delimiter, add it to the list
					send.clear();//start on the next word
				}
				
			}		
			return;
			return;
		}
		string join(){
			string out;
			int i;
			for (i = 0; i < size; i++) out += a[i];
			return out;
		}
		 
		void push(string in){
			string *buffer;
			buffer = new string[size];
			int i;
			for (i = 0; i < size; i++) buffer[i] = a[i];
			delete [] a;
			size++;
			a = new string[size];
			for (i = 0; i < size - 1; i++) a[i] = buffer[i];
			a[size - 1] = in;
			delete [] buffer;
			return;
		}
		void insert(int place, string in){
			if (place == size) {push(in); return;}
			if (place >= size || place < 0) return;
			string* buffer;
			buffer = new string[size];
			int i;
			for (i = 0; i < size; i++) buffer[i] = a[i];
			delete [] a;
			size++;
			a = new string[size];
			for (i = 0; i < place; i++) a[i] = buffer[i];
			a[place] = in;
			for (i = place + 1; i < size; i++) a[i] = buffer[i - 1];
			delete [] buffer;
			return;
		}
		void make(int in){
			if (in < 1) return;
			delete [] a;
			a = new string[in];
			return;
		}
		void assign(int place, string in){
			if (place >= size || place < 0) return;
			a[place] = in;
			return;		
		}
		void remove(int in){
			if (in < 0 || in >= size) return;
			string * buffer;
			buffer = new string[size];
			int i;
			for (i = 0; i < size; i++) buffer[i] = a[i];
			delete [] a;
			size--;
			a = new string[size];
			for (i = 0; i < in; i++) a[i] = buffer[i];
			for (i = in; i < size; i++) a[i] = buffer[i + 1];
			delete [] buffer;
			return;
		}		
		
		void clear(){delete [] a; size = 0; a = new string[1]; return;}
		int length(){int in; in = size; return in;}
		string view(int in){string out = ""; if (in < size && in >=0) out = a[in]; return out;}
		void list(){
			int i;
			for (i = 0; i < size; i++)
			{
				cout << "String " << i << " contains " << a[i] << '\n';
			}
			return;		
		}		
};

