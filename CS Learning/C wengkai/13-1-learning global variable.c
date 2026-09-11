#include <stdio.h>
int f(void);
int gAll=12;//全局变量默认初始化为0
//int g2=gAll;//只能用已知值初始化全局变量
int main(int argc,char const *argv[]){
    //printf("in %s gAll=%d\n",__func__,gAll);
    f();//f();f();
    //printf("agn in %s gAll=%d\n",__func__,gAll);
    return 0;
}
int f(void){
    //int gAll=1;//局部变量覆盖全局变量
    int k=1;//普通本地变量执行三次f为1 3;1 3;1 3
    static int all=1;//静态本地变量执行三次f为1 3;3 5;5 7
    printf("&gAll=%p\n",&gAll);//&gAll=00007FF736D53000
    printf("&all =%p\n",&all); //&all =00007FF736D53004  静态本地变量本质上是全局变量，生存期都是全局，区别是作用域
    printf("&k   =%p\n",&k);   //&k   =0000009D25FFF69C
    printf("in %s all=%d\n",__func__,all);
    //gAll+=2;
    all+=2;
    printf("agn in %s all=%d\n",__func__,all);
    return all;
}