precision highp float;
uniform vec2 resolution;
uniform vec3 eye;
uniform vec3 look;
uniform float time;
uniform float bend;
uniform float imageAlpha;
uniform float diskGain;
varying vec2 vUv;

float hash21(vec2 p){p=fract(p*vec2(123.34,456.21));p+=dot(p,p+45.32);return fract(p.x*p.y);}
float noise(vec2 p){vec2 i=floor(p),f=fract(p);f=f*f*(3.-2.*f);return mix(mix(hash21(i),hash21(i+vec2(1,0)),f.x),mix(hash21(i+vec2(0,1)),hash21(i+1.),f.x),f.y);}
float hash31(vec3 p){p=fract(p*.1031);p+=dot(p,p.yzx+33.33);return fract((p.x+p.y)*p.z);}
float noise3(vec3 p){vec3 i=floor(p),f=fract(p);f=f*f*(3.-2.*f);return mix(mix(mix(hash31(i),hash31(i+vec3(1,0,0)),f.x),mix(hash31(i+vec3(0,1,0)),hash31(i+vec3(1,1,0)),f.x),f.y),mix(mix(hash31(i+vec3(0,0,1)),hash31(i+vec3(1,0,1)),f.x),mix(hash31(i+vec3(0,1,1)),hash31(i+vec3(1,1,1)),f.x),f.y),f.z);}
vec3 sky(vec3 d){
  vec2 uv=vec2(atan(d.z,d.x),asin(clamp(d.y,-1.,1.)));
  vec3 col=vec3(.0022,.0048,.009);
  for(int j=0;j<2;j++){
    float scale=j==0?180.:420.;vec2 p=uv*scale;vec2 cell=floor(p);float h=hash21(cell+float(j)*32.);
    vec2 off=vec2(hash21(cell+14.7),hash21(cell-8.1));float r=length(fract(p)-off);
    float star=exp(-r*r*(j==0?920.:680.))*step(j==0?.978:.993,h);
    col+=star*mix(vec3(.42,.63,.81),vec3(.85,.68,.44),hash21(cell+5.))* (j==0?.7:.45);
  }
  float haze=noise(uv*4.)*noise(uv*12.);col+=vec3(.002,.0034,.005)*haze;
  return col;
}
vec3 emission(vec3 p,vec3 dir){
  float r=length(p.xz);float a=atan(p.z,p.x);
  float omega=1.8/pow(r,1.5);float ph=a-time*omega;
  float taper=smoothstep(2.95,3.22,r)*(1.-smoothstep(8.3,10.,r));
  // Thin, irregular azimuthal filaments. sin/cos close the angular noise seamlessly.
  vec2 flow=vec2(cos(ph),sin(ph));
  float n=.58*noise3(vec3(r*18.,flow*9.))+.29*noise3(vec3(r*40.,flow*17.))+.13*noise3(vec3(r*78.,flow*32.));
  float bands=.28+.07*sin(r*39.+n*2.+1.7*sin(ph*7.+r*2.));
  float turbulence=pow(n,1.7)*.75;
  float streak=pow(max(0.,sin(ph*17.+r*5.+n*4.)),10.);
  float temp=pow(3./max(r,3.),1.4);
  vec3 hot=mix(vec3(1.,.23,.035),vec3(1.,.72,.31),temp);
  vec3 tang=normalize(vec3(-p.z,0.,p.x));float doppler=pow(clamp(1.+.38*dot(tang,-normalize(dir)),.45,1.6),2.);
  float intensity=(bands*.8+turbulence*.9+streak*.13)*pow(3./r,1.65)*taper;
  return hot*intensity*2.9*doppler*diskGain;
}
vec3 accel(vec3 p,float angular){float r2=dot(p,p);return -1.5*angular*p/(r2*r2*sqrt(r2));}
void main(){
  vec2 xy=(2.*gl_FragCoord.xy-resolution)/resolution.y;
  vec3 fw=normalize(look-eye),right=normalize(cross(fw,vec3(0,1,0))),up=cross(right,fw);
  vec3 dir=normalize(fw+(.39*xy.x)*right+(.39*xy.y)*up);
  vec3 p=eye,v=dir;vec3 crossv=cross(p,v);float angular=dot(crossv,crossv)*bend;
  vec3 color=vec3(0.);float trans=1.;bool swallowed=false;
  for(int i=0;i<260;i++){
    float radius=length(p);
    if(radius<1.01){swallowed=true;break;}
    if(radius>48.&&dot(p,v)>0.)break;
    float dt=clamp(radius*.048,.035,1.2);
    vec3 a0=accel(p,angular);vec3 next=p+v*dt+.5*a0*dt*dt;
    vec3 a1=accel(next,angular);vec3 vn=v+.5*(a0+a1)*dt;
    if(p.y*next.y<0.){
      float q=abs(p.y)/(abs(p.y)+abs(next.y));vec3 hit=mix(p,next,q);float r=length(hit.xz);
      if(r>2.95&&r<10.){vec3 e=emission(hit,v);color+=trans*e;trans*=.14;}
    }
    p=next;v=vn;
  }
  if(!swallowed)color+=sky(normalize(v))*trans;
  // Angular photon trajectories form the disk images; there is no painted-on ring.
  color=vec3(1.)-exp(-color*1.05);color=pow(color,vec3(.4545));
  float vignette=1.-.18*pow(length(xy)/2.1,2.);
  color*=vignette;
  gl_FragColor=vec4(color,imageAlpha);
}
