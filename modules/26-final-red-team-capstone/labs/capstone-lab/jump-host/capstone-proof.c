#include <stdio.h>
#include <stdlib.h>
int main(void){
  FILE *f=fopen("/root/internal-token.txt","r");
  if(!f){perror("proof"); return 1;}
  char buf[256]={0};
  if(fgets(buf,sizeof(buf),f)) printf("%s",buf);
  fclose(f); return 0;
}
