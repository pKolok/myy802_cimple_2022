program test
{
	# declarations #
	declare x, y;
	declare i;
	
	function fun1 (in x)
	{
		x := x + 1;
		
		switchcase
		case (x <> 0)
			print(x);
		case (y = 0)
		{
			y := y - 1;
		}
		case (x=0)
			return(fun1(in 0));
		default
		{ return(x) }
	}
	
	procedure fun2 (inout x)
	{
		incase
		case (y < 0)
			print(y);
		case (y = 0)
		{
			y := 10;
			return(y)
		}
	}

	# main #
	input(x);
	input(y);
	
	i := fun1(inout x);
	call fun2(in -10);
	
	print(x); print(y);
}.