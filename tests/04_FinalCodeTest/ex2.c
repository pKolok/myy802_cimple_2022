program ex1
{  
	declare a,A,B;

	procedure f1(in a, inout b)
	{  
		procedure f2()
		{
			B:=A;
			b:=a;
		}

		A:=2;
		call f2();
	}

	# main #
	a:=3; A:=4;
	call f1(in a, inout A);
	print(A); print(B);
}.