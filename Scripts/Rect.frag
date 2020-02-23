float rect(in vec2 st, in vec2 size){
	size = 0.25-size*0.25;
    vec2 uv = step(size,st*(1.0-st));
	return uv.x*uv.y;
}