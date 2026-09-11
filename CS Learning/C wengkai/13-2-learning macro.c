#include <stdio.h>//#语句是编译预处理语句
#define PI 3.14159//等效于const double PI=3.14159;这里定义的PI就是宏(macro)
#define FORMAT "%f\n"
#define PI2 2*PI
#define PRT printf(FORMAT,PI);\
            printf(FORMAT,PI2)
#define cube(x) ((x)*(x)*(x))
#define radtodeg1(x) (x*57.29578)
#define radtodeg2(x) (x)*57.29578//注意一切都要有括号
int main(){
    //printf(FORMAT,PI2*3.0);
    //PRT;
    //int i;
    //scanf("%d",&i);
    //printf("%d\n",cube(i+2));
    printf(FORMAT,radtodeg1(5+2));
    printf(FORMAT,radtodeg1(7));
    printf(FORMAT,radtodeg2(5+2));
    printf(FORMAT,radtodeg2(7));
    printf(FORMAT,180/radtodeg1(1));
    printf(FORMAT,180/radtodeg2(1));
    return 0;
}