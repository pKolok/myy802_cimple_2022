program ex1
{  
	declare a,A,B;

	procedure f1()
	{  
		procedure f2(in a, inout b)
		{
			B:=A;
			b:=a;
		}

		A:=2;
		call f2(in a, inout A);
	}

	# main #
	a:=3; A:=4;
	call f1();
	print(A); print(B);
}.