program ex1
{
	declare b,c,g; 
	
	function P1(in X,inout Y) 
	{ 
	Y:=Y-1; 
	if (X=1) 
		return(X); 
	else 
		return(P1(in X-1,inout Y)); 
	} 
	c:=10; 
	b:=5; 
	g:=P1(in c, inout b); 
}.