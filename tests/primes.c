program primes
{
	# declarations for main #
	declare i;

	function isPrime(in x)
	{
		# declarations for isPrime #
		declare i;

		function divides(in x, in y)
		{
			# body of divides #
			if (y = (y/x)*x)
				return (1);
			else
				return (0);
		}

		# body of isPrime #
		i:=2;
		while (i<x)
		{
			if (divides(in i, in x)=1)
				return(0);;
			i := i + 1
		};
		return(1)
	}

	# body of main #
	i := 2;
	while (i<=30)
		if (isPrime(in i)=1)
			print(i);;
}.