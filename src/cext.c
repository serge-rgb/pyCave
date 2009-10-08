#include<stdio.h>
#include<GL/gl.h>

void sendVertex (double  *nx,double *x){
  glNormal3dv(nx);
  glVertex3dv(x);
}
