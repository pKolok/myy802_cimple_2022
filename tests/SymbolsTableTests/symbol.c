program symbol
{ 
	const A=1;
	declare a,b,c;

	procedure P1(in x, inout y)
	{ 
		declare a;

		function F11(in x);
		{
			declare a;
			
			# body of F11 #
			b = a;
			a = x;
			c = F11(in x);
			return (c);
		}

		function F12(in x)
		{ 
			# body of F12 #
			c = F11(in x);
			return (c);
		}

		# body of P1 #
		y = x;
	}

	procedure P2(inout x)
	{ 
		declare x;
		# body of P2 #
		y = A;
		call P1(in x, inout y);
	}

	# main program #
	call P1(in a, inout b);
	call P2(in c);

}