#ifndef GROUPCLASS_H
#define GROUPCLASS_H
#include <math.h>
#include <algorithm>
#include <iostream>

class Group
{
	friend class Set;
	private:
		int modulus;
		int canon_tto;
		int default_m;
		bool ordered;
		bool multiset;
		int base;

		long long int* dec_list;
		long long int* sc_list;
		int iter;
		int size;

		void reset(){
			iter = 0; size = 1;
			current = new Set[size];
			dec_list = new long long int[size];
			sc_list = new long long int[size];

			mod(12);
			canon(1);
			m_value(5);
			order(true);
			multi(false);
			base_value(2);

			return;
		
		};
	public:

		Set* current;
		Group(){reset(); return;}
		~Group(){
			delete [] current; delete [] dec_list; delete [] sc_list;
		}
		Group& operator= (const Group &a){
			if(this == &a) return *this;
			
			size = a.size;
			iter = a.iter;
			ordered = a.ordered;
			canon_tto = a.canon_tto;
			multiset = a.multiset;
			modulus = a.modulus;
			delete [] dec_list;
			delete [] sc_list;
			delete [] current;
			dec_list = new long long int[size];
			sc_list = new long long int[size];
			current = new Set[size];
			int i;
			for (i = 0; i < size; i++)
			{
				current[i] = a.current[i];
				dec_list[i] = a.dec_list[i];
				sc_list[i] = a.sc_list[i];
			}

			return *this;

		};
       
		
		void clear(){
			delete [] dec_list;
			delete [] sc_list;
			delete [] current;
			reset();
			return;
		};
		//like add_set but adds many at a time. (any old sets are deleted)
	
		void make(int howmany){

			size = howmany;
			delete [] current;
            current = new Set[size];
			iter = 0;
			//refresh_list();
		};
        void add_set(){

            Set* buffer;
            buffer = new Set[size];
            int i;
            for (i = 0; i < size; i++){buffer[i] = current[i];}
            delete [] current;
            size++;
            current = new Set[size];
			
            for (i = 0; i < size - 1; i++){current[i] = buffer[i];}
            delete [] buffer;
            iter = size -1;
            refresh_list();
            return;

        };
        void insert_set(int number){

            if (number > size) number = size;
            if (number < 0) number = 0;
            Set* buffer;
            buffer = new Set[size];
            int i;
            for (i = 0; i < size; i++)
            {
                buffer[i]=current[i];
            }
            delete [] current;
            size++;
            current = new Set[size];
            for (i = 0; i < number; i++)
            {
                current[i] = buffer[i];
            }
            for (i = number + 1; i < size; i++)
            {
                current[i] = buffer[i - 1];
            }
            delete [] buffer;
            iter = number;
            refresh_list();
            return;

        };
        void remove_set(int number){

            if (size == 1) {current[iter].clear(); return;}
            Set* buffer;
            buffer = new Set[size];
            if (number < 0) number = 0;
            int i;

            for (i = 0; i < size; i++)
            {
                buffer[i] = current[i];
            }
            //contract memory for current
            delete [] current;
            size = size - 1;
            if (number > size) number = size;
            current = new Set[size];
            //copy the sets before number
            for (i = 0; i < number; i++)  { current[i] = buffer[i]; }
            // copy the sets after the number
            for (i = number; i < size; i++) { current[i] = buffer[i + 1]; }
            delete [] buffer;

            if (iter >= size) iter = size - 1;

            refresh_list();
            return;

        };
        void swap_set(int num, int num2) {
            if (num < 0 || num2 < 0 || num >= size || num2 >= size) return;

            swap(current[num],current[num2]);

            refresh_list();
            return;
        };
        void swap(Set &a, Set &b) {Set c; c = a; a = b; b = c;}
        
        void equals_set(int num, int num2){
            if (num < 0 || num >= size || num2 < 0 || num2 >= size) return;
            current[num] = current[num2];
            return;
        }

        void next_set(){if (iter + 1 < size) iter++;};
        void prev_set(){if (iter - 1 >= 0) iter--;};
        void select_set(int number){if (number >= 0 && number < size) iter = number;};


        void mod(int newmod){

            if (newmod < 1) newmod = 1;
            if (newmod > MOD_LIMIT) newmod = MOD_LIMIT;
			modulus = newmod;
            int i;
            for (i = 0; i < size; i++)
            {
                current[i].change_mod(newmod);
            }

            refresh_list();
            return;

        };
		void canon(int value){
			if (value < 0 || value > 3) return;
			canon_tto = value;
			int i;
			for(i = 0; i < size; i++)
			{
				current[i].change_canon(value);
			}
			refresh_list();
			return;
		};
		void m_value(int value){
			if ( value < 1 || value > modulus) return;
			default_m = 5;
			int i;
			for (i = 0; i < size; i++)
			{
				current[i].change_m(value);
			}
			refresh_list();
			return;
		};
		void order(){if (ordered == true) {order(false); return;}if (ordered == false) order(true); return;};
		void order(bool value){
			ordered = value;
			current[0].change_order(value);
			return;
		};
		void multi(){if (multiset == true) {multi(false); return;}if (multiset == false) multi(true); return;};
		void multi(bool value){
			multiset = value;
			current[0].change_multi(value);
			return;

		};
		void base_value(int value){
			base = value;
			int i;
			for (i = 0; i < size; i++)
			{
				current[i].change_base(value);
			}
			refresh_list();
			return;
		};
		
		
       
        void update_list(int number){
            if (number < 0 || number >= size) {refresh_list(); return;}
            dec_list[number] = current[number].get_integer();
            sc_list[number] = current[number].get_sc_integer();
            return;

        };
        void refresh_list(){

            delete [] dec_list;
            delete [] sc_list;
            dec_list = new long long int[size];
            sc_list  = new long long int[size];
            int i;
            for (i = 0; i < size; i++)
            {
                dec_list[i] = current[i].get_integer();
                sc_list[i] = current[i].get_sc_integer();
            }
            return;
        };

        //for output
        int get_iter() {int r = iter; return r;};
        int get_size() {int r = size; return r;};


		int get_modulus() {int r = modulus; return r;};
		int get_canon() {int r = canon_tto; return r;};
		int get_default_m() {int r = default_m; return r;};
		bool get_ordered() {bool r = ordered; return r;};
		bool get_multiset() {bool r = multiset; return r;};
		int get_base(){int r = base; return r;};


        long long int* get_dec_list() {
            long long int* answer;
            answer = new long long int[size];
            int i;
            for (i = 0; i < size; i++)
            {
                *(answer + i) = sc_list[i];
            }
            return answer;
        };
        long long int* get_sc_list() {
            long long int* answer;
            answer = new long long int[size];
            int i;
            for (i = 0; i < size; i++)
            {
                *(answer + i) = dec_list[i];
            }
            return answer;

        };

};

#endif
