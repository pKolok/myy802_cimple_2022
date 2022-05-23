program gnlvCode
{
	function f1()
	{
		declare x;
		
		function f2()
		{
			function f3()
			{
				x := 1;
				return(x);
			}
			return(f3());
		}
		return(f2());
	}
	print(f1());
}.