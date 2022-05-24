program ex1
{  
	declare A,B;

	procedure f1(inout A)
	{  
		declare x;
		
		procedure f2 ()
		{
			procedure f3(in a, inout b)
			{
				B:=A;
				b:=a;
			}
			
			call f3(in x, inout A);
		}

		x:=3; A:=2;
		call f2();
		print(A); 
	}

	# main #
	call f1(inout A);
	print(B);
}.