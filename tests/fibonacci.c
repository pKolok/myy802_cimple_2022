program fibonacci
{
	declare x;
	
	function fibonacci(in x)
	{
		return (fibonacci(in x-1)+fibonacci(in x-2));
	}
	
	# main #
	input(x);
	print(fibonacci(in x));
}.