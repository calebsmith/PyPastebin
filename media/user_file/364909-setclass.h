#ifndef SETCLASS_H
#define SETCLASS_H
const bool DEBUG = 0;
#include <math.h>
#include <algorithm>
#include <iostream>
#include <string>

using namespace std;

const int PITCH_LIMIT = 640;
const int MOD_LIMIT = 31;
 

class Set
{
	private:
		int* plist;
		int* pclist;
		int pitch;
		int length;
		int pitch_class;  
		int* pc_array;
		int* sc_array;
		int* temp_array;
		int* icv;
		int* temp_icv;
		long long int setint;
		long long int scint;
		long long int comset;
		long long int mset;
		long long int zset;
		int cardinality;
		string fname;
                       
		static int Modulus;              
		static int Canon;
		static int Default_M;
		static int Ordered;
		static int Multi;
		static int Base;

		//derive internal values
		void findpc() {int r = findpc(pitch); pitch_class = r; return;};
		int findpc(int p){
			while (p >=Modulus) { p = p - Modulus;};
			while (p < 0) { p = p + Modulus;};
			return p;
		};
		void findbool(){
			int i;
			int thispc;
			for (i = 0; i < Modulus; i++)//reset to 0
			{
				pc_array[i] = 0;
			}
			for (i = 0; i < length; i++)//mark 1 if pc is present
			{                        
				thispc = pclist[i];
				pc_array[thispc] = 1;
			}
		};
		void findcardinality(){
			int i;
			cardinality = 0;
			for (i = 0; i < Modulus; i++)
			{
				if (pc_array[i] >= 1) cardinality+=1;
			}

		};
		int findcardinality(int intin){
			
			int i;
			int tempcard = 0;
			int* set;
			set = new int[Modulus];
			to_binary(intin);
			for (i = 0; i < Modulus; i++){set[i] = temp_array[i];}
			for (i = 0; i < Modulus; i++)
			{
				if (set[i] >= 1) tempcard+=1;
			}
			delete [] set;
			return tempcard;
		};

		long long int transpose_int(long long int intin, int shift){
			long long int answer;
			int i, i2;
			int* set;
			int* tempset;
			set = new int [Modulus];
			tempset = new int [Modulus];
                  
			to_binary(intin);
			for (i = 0; i <Modulus; i++){set[i] = temp_array[i];}
			for (i = 0; i < Modulus; i++)
			{
				i2 = i + shift;
				while (i2 >= Modulus){i2 = i2 - Modulus;};
				while (i2 < 0){i2 = i2 + Modulus;};
				tempset[i2] = set[i];
			}
			answer = to_decimal(tempset, Modulus);
			delete [] set;
			delete [] tempset;
			return answer;
		};

		long long int inversion_int(long long int intin){
			long long int answer;
			int i, i2;
			int* set;
			int* tempset;
			set = new int[Modulus];
			tempset = new int[Modulus];
			to_binary(intin);
			for (i = 0; i <Modulus; i++){set[i] = temp_array[i];}
			for (i = 0; i < Modulus; i++)
			{
				i2 = (Modulus - 1) - i; if (i2 == Modulus) i2 -= Modulus;
				tempset[i2] = set[i];
			}
			answer = to_decimal(tempset, Modulus);
			delete [] set;
			delete [] tempset;
			return answer;
		};
		long long int m_int(long long int intin){long long int r = m_int(intin, Default_M);return r;};
		long long int mi_int(long long int intin){long long int r = m_int(intin, Modulus - Default_M); return r;};
		long long int m_int(long long int intin, int value){
			long long int answer;
			int i, i2;
			int* set;
			int* tempset;
			set = new int[Modulus];
			tempset = new int [Modulus];
			to_binary(intin);
			for (i = 0; i <Modulus; i++){set[i] = temp_array[i];}
			for (i = 0; i < Modulus; i++)
			{
				i2 = i * value;
				while (i2 >= Modulus){i2 -= Modulus;}
				tempset[i2] = set[i];
			}
			answer = to_decimal(tempset, Modulus);
			delete [] set;
			delete [] tempset;
			return answer;
		};

	
              //conduct a search for a pitch or pc
		void search(int search_num, bool pitchtype){
			int i;
			int i2 = 0;
			delete [] s.list;
			s.list = new long long int[length];

			for (i = 0; i < length; i++)
			{
				if (pitchtype == 0)
				{
					if (pclist[i] == search_num)
					{
						s.list[i2] = i;
						i2++;
					}	
				}
				if (pitchtype == 1)
				{
					if (plist[i] == search_num)
					{
						s.list[i2] = i;
						i2++;
					}
				}
			}
			s.size = i2;
			return;
		};
		void derive_pitches(int intin){
				int i,i2;
				delete [] pc_array;
				pc_array = new int[Modulus];
				to_binary(intin);
				for (i = 0; i <Modulus; i++){pc_array[i] = temp_array[i];}
				int newcard = 0;
				newcard = findcardinality(intin);
				length = newcard;	
				i2 = 0;
				
				delete [] plist; delete [] pclist;
				plist = new int[newcard];
				pclist = new int[newcard];
				for (i = 0; i < Modulus; i++)
				{
					if (pc_array[i] >= 1) 
					{
						plist[i2] = i;
						pclist[i2] = i;
						i2++;
					}
				}
		};
		void reset(){
			int i;
			pitch = 0;
			pitch_class = 0;
			setint= 0;
			scint = 0;
			comset = 0;
			mset = 0;
			zset = -1;
			length = 0;
			cardinality = 0;
			fname = "";
			plist = new int[1];
			pclist = new int[1];
			s.list = new long long int[1];
			tto.list = new long long int[1];
			embedded.list = new long long int[1];
			pc_array = new int[Modulus];
			sc_array = new int[Modulus];
			temp_array = new int[Modulus];
			icv = new int[(Modulus / 2) + 1];
			temp_icv = new int[(Modulus / 2) + 1];
			for (i = 0; i < Modulus; i++)
			{
				pc_array[i] = 0;
				sc_array[i] = 0;
				temp_array[i] = 0;
			}
			for (i = 0; i < (Modulus / 2) + 1; i++)
			{
				icv[i] = 0;
				temp_icv[i] = 0;
			}
			refresh();
		};
	protected:
             
	public:
              
			struct list_answer{
				long long int* list;
				int size;
			} s, tto, embedded;
	      	//constructor, destrcutor, copier, and equals overload 
			Set() {reset();};

			~Set() {
				delete [] pc_array; delete [] sc_array; delete [] temp_array; delete [] icv; delete [] temp_icv;
						delete [] plist; delete [] pclist;delete [] s.list; delete [] tto.list; delete [] embedded.list; 
			};	
			void clear(){
				delete [] plist; delete [] pclist; 
				delete [] pc_array; delete [] sc_array; delete [] icv; delete [] temp_icv;
		
				delete [] s.list;
				delete [] tto.list;
				delete [] embedded.list;
			
				delete [] temp_array;
				reset();
			};

			Set(const Set& a){
				delete [] plist; delete [] pclist;
				delete [] pc_array; delete [] sc_array; delete [] temp_array;
				delete icv; delete [] temp_icv;
				delete [] tto.list;	tto.list = new long long int[1];
				delete [] s.list; s.list = new long long int[1];
				delete [] embedded.list; embedded.list = new long long int[1];
				
				length = a.length;
				plist = new int[length];
				pclist = new int[length];

				int i;
				for (i = 0; i < length; i++)
				{
					plist[i] = a.plist[i];
					pclist[i] = a.pclist[i];
				}

				Modulus = a.Modulus;
				Canon = a.Canon;
				Ordered = a.Ordered;
				Default_M = a.Default_M;
				Multi = a.Multi;

				pc_array = new int [Modulus];
				sc_array = new int [Modulus];
				temp_array = new int [Modulus];
				icv = new int [(Modulus / 2) + 1];
				temp_icv = new int [(Modulus / 2) + 1];
				for (i = 0; i < Modulus; i++)
				{
					pc_array[i] = a.pc_array[i];
					sc_array[i] = a.sc_array[i];
					temp_array[i] = a.temp_array[i];
				}
				for (i = 0; i < (Modulus / 2) + 1; i++)
				{
					icv[i] = a.icv[i];
					temp_icv[i] = a.temp_icv[i];
				}

				setint = a.setint;
				scint = a.scint;
				comset = a.comset;
				mset = a.mset;
				zset = a.zset;
				cardinality = a.cardinality;
				fname = a.fname;
			};

              
			Set& operator= (const Set &a){
				if(this == &a) return *this;

				delete [] plist; delete [] pclist;
				delete [] pc_array; delete [] sc_array; delete [] temp_array;
				delete [] icv; delete [] temp_icv;
				delete [] tto.list;	tto.list = new long long int[1];
				delete [] s.list; s.list = new long long int[1];
				delete [] embedded.list; embedded.list = new long long int[1];
				
				length = a.length;
				plist = new int[length];
				pclist = new int[length];
				int i;
				for (i = 0; i < length; i++)
				{
					plist[i] = a.plist[i];
					pclist[i] = a.pclist[i];
					
				}

				Modulus = a.Modulus;
				Canon = a.Canon;
				Ordered = a.Ordered;
				Default_M = a.Default_M;
				Multi= a.Multi;

				pc_array = new int [Modulus];
				sc_array = new int [Modulus];
				temp_array = new int [Modulus];
				icv = new int [(Modulus / 2) + 1];
				temp_icv = new int [(Modulus / 2) + 1];
				for (i = 0; i < Modulus; i++)
				{
					pc_array[i] = a.pc_array[i];
					sc_array[i] = a.sc_array[i];
					temp_array[i] = a.temp_array[i];
				}
				for (i = 0; i < (Modulus / 2) + 1; i++) 

				{
					icv[i] = a.icv[i];
					temp_icv[i] = a.temp_icv[i];
				}
				setint = a.setint;
				scint = a.scint;
				comset = a.comset;
				mset = a.mset;
				zset = a.zset;
				cardinality = a.cardinality;
				fname = a.fname;
				return *this;
			};
		void make(int size){
			delete [] pclist; delete [] plist;
			length = size;
			plist = new int[length];
			pclist = new int[length];
			return;
		};
        void assign(int list_number, int number){
			if (list_number > length) add(number);
			if (list_number < 0) return;
			pitch = number;
			while (pitch > PITCH_LIMIT) {pitch-= Modulus;}
			while (pitch < -PITCH_LIMIT) {pitch+= Modulus;}
			plist[list_number] = pitch;
			pclist[list_number] = findpc(pitch);
			return;			
		};

		//assign a pitch to the set object w/ add. Others include insert, remove, and swap_p

		void add(int number){
			int i;
			int temp_pc;
			//if multisets are off, check for pitch already in set
			if(Multi == false){
			    for (i = 0; i < length; i++){
				    temp_pc = findpc(plist[i]);
				    if (number == plist[i] || number == temp_pc) return;
			    }				
			}
			int* pbuffer;
			pbuffer = new int[length];
			for (i = 0; i < length; i++){pbuffer[i] = plist[i];}
			delete [] pclist;
			delete [] plist;

			pclist = new int[length + 1];
			plist = new int[length + 1];
			for (i = 0; i < length; i++)
			{
				plist[i] = pbuffer[i];
				pclist[i] = findpc(plist[i]);
			}
			delete [] pbuffer;
			pitch = number;
			while (pitch > PITCH_LIMIT) {pitch-= Modulus;}
			while (pitch < -PITCH_LIMIT) {pitch+= Modulus;}
			plist[length] = pitch;
			pclist[length] = findpc(pitch);
			length++;
			refresh();
			return;
		};
		//remove a pitch/pc from the corresponding list. parameter is number in list
		void remove(int list_number){
			//make sure parameter is within bounds and there is an element to remove
			if (length < 1 || list_number < 0 || list_number >= length) return;
			int i;
			int* pbuffer;
			pbuffer = new int[length];
			for (i = 0; i < length;i++)
			{
				pbuffer[i]=plist[i];
			}
			delete [] plist;
			delete [] pclist;
			length--;
			pclist= new int[length];
			plist = new int[length];
			for (i = 0; i< list_number;i++)
			{
				plist[i] = pbuffer[i];
				pclist[i] = findpc(pbuffer[i]);
			}
			for (i = list_number; i < length; i++)
			{
				plist[i] = pbuffer[i + 1];
				pclist[i] = findpc(pbuffer[i + 1]);

			}
			delete [] pbuffer;

			refresh();
			return;
		};
		void insert(int number, int list_number){
			if (list_number < 0) return;
			if (length < 1 || list_number >= length) {add(number); return;}
			int i, temp_pc;
			if(Multi == false)
			{
			for (i = 0; i < length; i++)
			{
				temp_pc = findpc(plist[i]);
				if (number == plist[i] || number == temp_pc) return;
			}				
			}

			int* pbuffer;
			pbuffer = new int[length];
			for (i = 0; i < length; i++)
			{
				pbuffer[i] = plist[i];
			}
			delete [] plist;
			delete [] pclist;
			length++;
			pclist= new int[length];
			plist = new int[length];
			for (i = 0; i < list_number; i++)
			{
				plist[i] = pbuffer[i];
				pclist[i] = findpc(pbuffer[i]);
			}
			plist[list_number] = number;
			pclist[list_number] = findpc(number);
			for (i = list_number + 1; i < length; i++)
			{
				plist[i] = pbuffer[i - 1];
				pclist[i] = findpc(pbuffer[i - 1]);
			}
			delete [] pbuffer;
			refresh();
			return;

		};
		void swap_p(int num, int num2){
			if (num < 0 || num2 < 0 || num >= length || num2 >= length) return;
			//swap pitches in list
			int temp = plist[num];
			plist[num] = plist[num2];
			plist[num2] = temp;
			//swap pitch classes in list
			int temp_pc = pclist[num];
			pclist[num] = pclist[num2];
			pclist[num2] = temp_pc;
			return;
		};
		//change status for individual set, what has been changed for the whole group
		void change_mod(int newmod){
			delete [] pc_array;
			delete [] sc_array;
			delete [] temp_array;
			delete [] icv;
			delete [] temp_icv;
			Modulus = newmod;
					   
			pc_array = new int [Modulus];
			sc_array = new int [Modulus];
			temp_array = new int [Modulus];
			icv = new int [(Modulus / 2) + 1];
			temp_icv = new int [(Modulus / 2) + 1];
			int i;
			for (i = 0; i < length;i++) {pclist[i] = findpc(plist[i]); }

			refresh();
			return;
		};   


		
		void change_canon(int value){
		    if (value < 0 || value > 3) return;
			Canon = value;
			refresh();
			return;			
		};

		void change_multi(bool value){
			Multi = value;
			return;
		};
		void change_order(bool value){
			if (value == 1 || value == 0) Ordered = value;
			return;		
		};
		void change_m(int value){
		    if (Default_M <= 0) return;
			Default_M = value;
			while (Default_M > Modulus){
			    Default_M -= Modulus;
		    }
			refresh();
			return;
		};
		//very experimental. NOT IMPLEMENTED
		void change_base(int value){
			Base = value;
			refresh();
			return;
		};
		void search_pc(int search_num){bool pitchtype = 0; search(search_num, pitchtype);};
		void search_p(int search_num){bool pitchtype = 1; search(search_num, pitchtype);};
		void search(int search_num) {bool pitchtype = 0; search(search_num, pitchtype);};


		//perform operations on the set
		long long int to_decimal(int[],int);
		void to_binary(long long int);
		//int* to_binary(long long int);
		void transpose(int value){
			int i;
			int temp;
			for (i = 0; i < length;i++)
			{
				temp = plist[i] + value;
				while (temp > PITCH_LIMIT) {temp = temp - Modulus;}
				while (temp < -PITCH_LIMIT) {temp = temp + Modulus;}
				plist[i] = temp;
				pclist[i] = findpc(plist[i]);
			}

			setint = transpose_int(setint, value);
		 	to_binary(setint);
			for (i = 0; i < Modulus; i++){pc_array[i] = temp_array[i];}
		};
		void invert(){
			int i;
			for (i = 0; i < length; i++)
			{
			  plist[i] = -plist[i];
			  pclist[i] = findpc(plist[i]);
			}

			setint = inversion_int(setint);
			to_binary(setint);
			for (i = 0; i < Modulus; i++){pc_array[i] = temp_array[i];}
			refresh();	

		};
		void multiply () {multiply(Default_M);};
		void multiply(int value){
		int i;
		int temp;
		for (i = 0; i < length; i++)
		{
			temp = plist[i] * value;
			while (temp > PITCH_LIMIT) {temp-= Modulus;}
			while (temp < -PITCH_LIMIT) {temp += Modulus;}
			plist[i] = temp;
			pclist[i] = findpc(plist[i]);
		}

		setint = m_int(setint);
		to_binary(setint);
		for (i = 0; i < Modulus; i++){pc_array[i] = temp_array[i];}
		refresh();				

		};
		void refresh(){
			
			findbool();
			findcardinality();
			setint = to_decimal(pc_array, Modulus);
			prime();
			fortename();
			findicv();
			compliment();
			mpartner();
			//zpartner();
			if (Modulus <= 12) zpartner();
			if (Modulus > 12) zset = -1;
			
		};
		void prime() {scint = prime(setint); int i; to_binary(scint);
				for (i = 0; i < Modulus; i++){sc_array[i] = temp_array[i];}};
		long long int prime(long long int intin);

		void findicv(){findicv(scint);int i; for(i= 0; i < (Modulus / 2) + 1;i++){icv[i] = temp_icv[i];} return;};
		void findicv(long long int intin);
		//int* findicv(long long int intin);

		void fortename(){fname = fortename(scint); return;};
		string fortename (long long int);
		long long int fname_to_scint(string fnamein);

		void set_from_fname(string fnamein){
			long long int val;
			val = fname_to_scint(fnamein);	
			if (val < 0 || val > 4095) return;
			if (Modulus != 12 || Canon != 1) {return;}

			clear();
			derive_pitches(val);
			refresh();

			return;

		};
		void set_from_int(long long int intin){
			clear();
			derive_pitches(intin);
			refresh();
		};
		void set_from_z(){
			if (zset != -1)
			{
				long long int z = zset;//stored before set is cleared
				clear();
				derive_pitches(z);
				refresh();
			}			
		};
		void set_from_c(){
			long long int c = comset; //store before clearing the set
			clear();
			derive_pitches(c);
			refresh();
		};
		void compliment(){comset = abstract_compliment(scint); return;};
		long long int compliment(long long int intin){long long int r; r = abstract_compliment(intin); return r;};
	
		long long int literal_compliment(long long int intin){
			long long int answer;
			int* set;
			int* temp;
			set = new int[Modulus];
			temp = new int[Modulus];
			int i;				
			to_binary(intin);
			for (i = 0; i < Modulus; i++){set[i] = temp_array[i];}			
			for (i = 0; i < Modulus; i++)
			{
				if (set[i] == 0) temp[i] = 1;
				if (set[i] == 1) temp[i] = 0;
			}
			delete [] set;
			answer = to_decimal(temp,Modulus);
			delete [] temp;
			return answer;
		};
		long long int abstract_compliment(long long int intin){
			long long int answer;
			long long int tempdec;
			tempdec = literal_compliment(intin);
			answer = prime(tempdec);
			return answer;			
		};
		void mpartner(){mset = mpartner(setint); return;};
		long long int mpartner(long long int intin){
			long long int answer;
			answer = prime(m_int(intin));
			return answer;
		};
	
		void zpartner() {zset = zpartner(setint); return;};
		long long int zpartner(long long int);
		
		long long int lowest(long long int* listofints, int size);
		void all_tto(long long int);
		
		//for output 
		int get_p(int p){int r; r = plist[p]; return r;};
		int get_pc(int p) {int r; r = pclist[p]; return r;};    
		int* get_binary() {
			int* answer;
			answer = new int[Modulus];
			int i;
			for (i = 0; i < Modulus; i++)
			{
				*(answer + i) = pc_array[i];
			}
			return answer;
		};
		int* get_binary_fixed(){
			int* answer; answer = new int[Modulus];
			answer = get_fixed(pc_array);
			return answer;
		};
		int* get_sc() {
			int* answer;
			answer = new int[Modulus];
			int i;
			for (i = 0; i < Modulus; i++)
			{
			  *(answer + i) = sc_array[i];
			}
			return answer;
		};
		int* get_sc_fixed() {
			int* answer; answer = new int[Modulus];
			answer = get_fixed(sc_array);
			return answer;
			
		};
			
		string list_string(int* list, int style, int size){
			string answer;
			if (size == 0)
			{
				if (style == 0 || style == 2) size = get_card();
				if (style == 1) size = get_length();
				if (style == 3) size = (Modulus / 2) + 1;
				if (style > 3) return "error - no size specified";
			}
			
			int* temp_list;
			temp_list = new int[size];
			int i, i2;
			for (i = 0; i < size; i++) {temp_list[i] = list[i];}
			if (style == 0) answer += "{";
			if (style == 1) answer += "<";
			if (style == 2) answer += "(";
			
			for (i = 0; i < size; i++)
			{
				
					if (list[i] < 10) answer += char(list[i] + '0');
					if (list[i] > 9 )
					{
						for (i2 = 0; i2 < list[i] / 10; i2++)
						{
							if (i2 == (list[i] /10) - 1)
							{
								answer += char((i2 + 1)+ '0');
								answer += char((list[i] - ((i2 +1)* 10)) + '0');
							}							
						}
					}
				
				if (style != 3 && i < size - 1) answer += ",";
			}
			if (style == 0) answer += "}";
			if (style == 1) answer += ">";
			if (style == 2) answer += ")";
			delete [] temp_list;
			return answer;		
		};
		string list_string(int* list){string r;r = list_string(list, 0, 0);return r;};
		string list_string(long long int intin){string r;r = list_string(intin, 0, 0);return r;};
		string list_string(int* list, int style) {string r; r = list_string(list, style,0); return r;};
		string list_string(long long int intin, int style) {string r; r = list_string(intin,style,0); return r;};
		string list_string(long long int intin, int style, int size){
			string answer;
			if (intin == -1) return "none";
			if (intin == 0 && style == 0) return "{}";
			if (intin == 0 && style == 1) return "<>";
			if (intin == 0 && style == 2) return "()";
			int* list;
			list = new int[Modulus];
			to_binary(intin);
			int i,i2;
			i2 = 0;
			for (i = 0; i < Modulus; i++) 
			{
				if (temp_array[i] > 0) 
				{
					list[i2] = i;
					i2++;
				}
				
			}
			size = findcardinality(intin);
			answer = list_string(list,style, size);			
			delete [] list;
			return answer;		
		};
		
		int* list_int(long long int intin){
			int* answer;
			answer = new int[Modulus];
			
			return answer;
		};
		int* get_fixed(int* list){
			int* answer;
			answer = new int[Modulus];
			int i,i2;			
			i2 = 0;
			for (i = 0; i < Modulus; i++)
			{
				if (list[i] > 0) {answer[i2] = i; i2++;}				
			}					
			return answer;
		}
             
		long long int get_integer() {long long int r = setint; return r;};
		int get_modulus() {int r = Modulus; return r;};
		long long int get_sc_integer() {long long int r = scint; return r;};
		string get_fname() {string r = fname; return r;};
		int get_cardinality() {int r = get_card(); return r;};
		int get_card() {int r = cardinality; return r;};
		int get_length() {int r = length; return r;};
		//int get_icv(int n){int r = icv[n]; return r;};
		int* get_icv(){int* r; r = new int[Modulus / 2 +1]; 
				int i; for (i= 0; i < Modulus / 2 + 1; i++) {r[i] = icv[i];} return r;};
		int* get_icv(long long int intin){findicv(intin); int* r; r = new int[Modulus / 2 + 1];
				int i; for (i = 0; i < Modulus / 2 + 1; i++) {r[i] = temp_icv[i];} return r;};

		long long int get_compliment() {long long int r; r = comset; return r;};
        long long int get_mpartner() {long long int r; r = mset; return r;};
		long long int get_zpartner() {long long int r; r = zset; return r;}; 
};


#include "groupclass.h"
#include "pageclass.h"

#endif
