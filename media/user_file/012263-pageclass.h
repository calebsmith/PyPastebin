#ifndef PAGECLASS_H
#define PAGECLASS_H
#include <math.h>
#include <algorithm>
#include <iostream>
#include <fstream>
#include <string.h>
#include <sstream>

using namespace std;

class Page{
	private:
		int tab_number;
		int tab_size;
	public:
		Group* tab;
		Page(){
			tab_size = 1;
			tab_number = 0;
			tab = new Group[tab_size];
		};
		~Page(){
			delete [] tab;
		};

        void swap_tab(int num, int num2) {
            if (num < 0 || num2 < 0 || num >= tab_size || num2 >= tab_size) return;

            swap(tab[num], tab[num2]);

            //refresh_tab();
            return;
        };
        void swap(Group &a, Group &b) {Group c; c = a; a = b; b = c;}
		
		void show(){stat(); list(); set();}; 
		void show(int var);
		void stat();
		void list();
		void set();
		void save();
		void save(string filename);
		void load();
		void load(string filename);

		void make(int* list, int size){
			int i;		
			make(size);			
			for (i = 0; i < size; i++)
			{
			    tab[i].make(list[i]);
			}
			return;
		};
		void make(int number){
			delete [] tab;
			tab_size = number;
			tab_number = tab_size - 1;
			tab = new Group[tab_size];
			return;
		};
		void add_tab(){
			Group* buffer;
			buffer = new Group[tab_size];
			int i;
			for (i = 0; i < tab_size; i++)
			{
				buffer[i] = tab[i];			
			}		
			delete [] tab;
			tab_size++;
			tab = new Group[tab_size];
			for (i = 0; i < tab_size - 1; i++)
			{
				tab[i] = buffer[i];				
			}
			tab_number = tab_size - 1;
			delete [] buffer;
			return;
		};
		void insert_tab(int list_number){
			if (list_number < 0 || list_number >= tab_size) return;
			Group* buffer;
			buffer = new Group[tab_size];
			int i;
			for (i = 0; i < tab_size; i++){buffer[i] = tab[i];}
			delete [] tab;
			tab_size++;
			tab = new Group[tab_size];
			for (i = 0; i < list_number; i++){tab[i] = buffer[i];}
			
			for (i = list_number + 1; i < tab_size; i++){tab[i] = buffer[i - 1];}
			delete [] buffer;
			tab_number = list_number;
			return;
		};
		void remove_tab(int list_number){
			if (tab_size <= 1 || list_number < 0 || list_number >= tab_size) return;
			Group* buffer;
			buffer = new Group[tab_size];
			int i;
			for (i = 0; i < tab_size; i++){ buffer[i] = tab[i];}		
			delete [] tab;
			tab_size--;
			tab = new Group[tab_size];
			for(i = 0; i < list_number; i++)
			{
				tab[i] = buffer[i];			
			}
			for (i = list_number; i < tab_size; i++)
			{
				tab[i] = buffer[i + 1];			
			}
			delete [] buffer;
			if (tab_number > 0) tab_number--;
			return;
		};
		void next_tab(){if (tab_number < tab_size - 1) tab_number++; return;};
		void prev_tab(){if (tab_number > 0) tab_number--; return;};
		void select_tab(int number){if (number >= 0 && number < tab_size) tab_number = number; return;};

		int get_tab_number(){int r = tab_number; return r;};
		int get_tab_size(){int r = tab_size; return r;};	


		//delegate to class Set via class Group
		void add(int number){int iter = tab[tab_number].get_iter(); 
				tab[tab_number].current[iter].add(number);tab[tab_number].update_list(iter); return;};
        void insert(int number, int list_number){int iter = tab[tab_number].get_iter(); 
				tab[tab_number].current[iter].insert(number, list_number);tab[tab_number].update_list(iter); 					return;};
        void swap_p(int num, int num2) {int iter = tab[tab_number].get_iter();
				tab[tab_number].current[iter].swap_p(num,num2);};
        void remove(int number){int iter = tab[tab_number].get_iter();
				tab[tab_number].current[iter].remove(number);tab[tab_number].update_list(iter); return;};
        void set_clear(){int iter = tab[tab_number].get_iter();
				tab[tab_number].current[iter].clear();tab[tab_number].update_list(iter); return;};


        void transpose(int number){int iter = tab[tab_number].get_iter();
				tab[tab_number].current[iter].transpose(number);tab[tab_number].update_list(iter); return;};
        void invert(){int iter = tab[tab_number].get_iter();
				tab[tab_number].current[iter].invert();tab[tab_number].update_list(iter); return;};
        void multiply(){int iter = tab[tab_number].get_iter();
				tab[tab_number].current[iter].multiply();tab[tab_number].update_list(iter); return;};
        
        void zpartner(){
            int iter = tab[tab_number].get_iter();
            tab[tab_number].current[iter].zpartner();
            //tab[tab_number].update_list(iter);
            return;
        }

     
		long long int prime(long long int intin){int iter = tab[tab_number].get_iter();
				long long int r; r = tab[tab_number].current[iter].prime(intin); return r;};
		string fortename (int num) {int iter = tab[tab_number].get_iter();
				string r; r = tab[tab_number].current[iter].fortename(num); return r;};
		int fname_to_scint(string fnamein){int iter = tab[tab_number].get_iter();
				int r; r = tab[tab_number].current[iter].fname_to_scint(fnamein); return r;};
		
		void set_from_fname(string fnamein){int iter = tab[tab_number].get_iter();
				tab[tab_number].current[iter].set_from_fname(fnamein); tab[tab_number].update_list(iter); return;};
		void set_from_int(long long int intin){int iter = tab[tab_number].get_iter();
				tab[tab_number].current[iter].set_from_int(intin); tab[tab_number].update_list(iter); return;};
		void set_from_z(){int iter = tab[tab_number].get_iter();
				tab[tab_number].current[iter].set_from_z(); tab[tab_number].update_list(iter); return;};
		void set_from_compliment(){int iter = tab[tab_number].get_iter();
				tab[tab_number].current[iter].set_from_c(); return;};
		void set_from_c(){int iter = tab[tab_number].get_iter();
				tab[tab_number].current[iter].set_from_c(); tab[tab_number].update_list(iter); return;};

		long long int compliment(long long int intin){int iter = tab[tab_number].get_iter();
				long long int r; r = tab[tab_number].current[iter].compliment(intin); return r;};
		long long int mpartner(long long int intin){int iter = tab[tab_number].get_iter();
				long long int r; r= tab[tab_number].current[iter].mpartner(intin); return r;};
		//long long int zpartner(long long int intin){int iter = tab[tab_number].get_iter();
			//	tab[tab_number].current[iter].zpartner(intin); return;};

        long long int get_integer(){int iter = tab[tab_number].get_iter();
				long long int r = tab[tab_number].current[iter].get_integer(); return r;};
        long long int get_sc_integer(){int iter = tab[tab_number].get_iter();
				long long int r = tab[tab_number].current[iter].get_sc_integer(); return r;};

        int* get_binary(){int iter = tab[tab_number].get_iter();
				int* answer = tab[tab_number].current[iter].get_binary(); return answer;};
		int* get_binary_fixed(){int iter = tab[tab_number].get_iter();
				int* answer = tab[tab_number].current[iter].get_binary_fixed(); return answer;};
        int* get_sc(){int iter = tab[tab_number].get_iter();
				int* answer = tab[tab_number].current[iter].get_sc(); return answer;};
		int* get_sc_fixed() {int iter = tab[tab_number].get_iter();
				int* answer = tab[tab_number].current[iter].get_sc_fixed(); return answer;};

		string list_string(long long intin){int iter = tab[tab_number].get_iter();
				string r; r = tab[tab_number].current[iter].list_string(intin, 0); return r;};
		string list_string(int* list) {int iter = tab[tab_number].get_iter();
	 			string r; r = tab[tab_number].current[iter].list_string(list, 0); return r;};
		string list_string(long long intin, int style){int iter = tab[tab_number].get_iter();
				string r; r = tab[tab_number].current[iter].list_string(intin, style); return r;};
		string list_string(int* list, int style){int iter = tab[tab_number].get_iter();
				string r; r = tab[tab_number].current[iter].list_string(list,style); return r;};

		string list_string(long long intin, int style, int size){int iter = tab[tab_number].get_iter();
				string r; r = tab[tab_number].current[iter].list_string(intin,style,size); return r;};
		string list_string(int* list, int style, int size) {int iter = tab[tab_number].get_iter();
				string r; r = tab[tab_number].current[iter].list_string(list,style,size); return r;};


		int* list_int(long long int intin){int iter = tab[tab_number].get_iter();
				int* answer = tab[tab_number].current[iter].list_int(intin); return answer;};
		int* get_fixed(int* list){int iter = tab[tab_number].get_iter();
				int* answer = tab[tab_number].current[iter].get_fixed(list); return answer;};

		string get_fname() {int iter = tab[tab_number].get_iter();
				string r = tab[tab_number].current[iter].get_fname(); return r;};

        int get_length(){int iter = tab[tab_number].get_iter();
				int r = tab[tab_number].current[iter].get_length(); return r;};
        int get_card(){int iter = tab[tab_number].get_iter();
				int r = tab[tab_number].current[iter].get_card(); return r;};
        int get_p(int number){int iter = tab[tab_number].get_iter();
				int r = tab[tab_number].current[iter].get_p(number); return r;};
        int get_pc(int number){int iter = tab[tab_number].get_iter();
				int r = tab[tab_number].current[iter].get_pc(number); return r;};
        int get_modulus(){int iter = tab[tab_number].get_iter();
				int r = tab[tab_number].current[iter].get_modulus(); return r;};
		
		void findicv(long long int intin){int iter = tab[tab_number].get_iter();
				tab[tab_number].current[iter].findicv(intin); return;};
		int* get_icv(){int iter = tab[tab_number].get_iter(); int* r; r = new int [get_modulus() / 2 + 1];
				r = tab[tab_number].current[iter].get_icv();
				return r;};
		int* get_icv(long long int intin){int iter = tab[tab_number].get_iter(); 
				int* r; r = new int [get_modulus() / 2 + 1];
				r = tab[tab_number].current[iter].get_icv(intin); 
				return r;};

		long long int get_compliment() {int iter = tab[tab_number].get_iter();
				long long int r; r = tab[tab_number].current[iter].get_compliment(); return r;};
        long long int get_mpartner() {int iter = tab[tab_number].get_iter();
				long long int r; r= tab[tab_number].current[iter].get_mpartner(); return r;};
		long long int get_zpartner() {int iter = tab[tab_number].get_iter();
				long long int r; r = tab[tab_number].current[iter].get_zpartner(); return r;};

		//delegate to Group class

		void add_set(){tab[tab_number].add_set(); return;};
		void insert_set(int list_number){tab[tab_number].insert_set(list_number); return;};
		void remove_set(int list_number){tab[tab_number].remove_set(list_number); return;};
		void swap_set(int num, int num2){tab[tab_number].swap_set(num,num2); return;};
		void equals_set(int num, int num2){tab[tab_number].equals_set(num, num2); return;};
		
		void next_set(){tab[tab_number].next_set(); return;};
		void prev_set(){tab[tab_number].prev_set(); return;};
		void select_set(int num){tab[tab_number].select_set(num); return;};

		void canon(int value){tab[tab_number].canon(value); return;};
		void mod(int value){tab[tab_number].mod(value); return;};
		void m_value(int value){tab[tab_number].m_value(value); return;};
		void order(){tab[tab_number].order(); return;};
		void order(bool value){tab[tab_number].order(value); return;};
		void multi(){tab[tab_number].multi(); return;};
		void multi(bool value){tab[tab_number].multi(value); return;};
		void base(int value){tab[tab_number].base_value(value); return;};

//output from group class


		int get_iter() {int r = tab[tab_number].get_iter(); return r;};
        int get_size() {int r = tab[tab_number].get_size(); return r;};
		
			
};

#endif
