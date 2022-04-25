int main()
{
int x,count,T_2,T_1;
L_100:                             // 100: begin_block, countDigits, _, _
L_101: scanf(%d, &x);              // 101: in, x, _, _           
L_102: count=0;                    // 102: :=, 0, _, count       
L_103: if (x>0) goto L_105;        // 103: >, x, 0, 105          
L_104: goto L_110;                 // 104: jump, _, _, 110       
L_105: T_1=x/10;                   // 105: /, x, 10, T_1         
L_106: x=T_1;                      // 106: :=, T_1, _, x         
L_107: T_2=count+1;                // 107: +, count, 1, T_2      
L_108: count=T_2;                  // 108: :=, T_2, _, count     
L_109: goto L_103;                 // 109: jump, _, _, 103       
L_110: printf(%d, count);          // 110: out, count, _, _      
L_111: return(0);                  // 111: halt, _, _, _         
L_112:                             // 112: end_block, countDigits, _, _
