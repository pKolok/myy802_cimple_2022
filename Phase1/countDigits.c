program countDigits
{
	declare x, count;

	# main #
	input(x);
	count := 0;
	while (x>0)
	{
		x := x/10;
		count := count+1;
	};
	print(count);
}.