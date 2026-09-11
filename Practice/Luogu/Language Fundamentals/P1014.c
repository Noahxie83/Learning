/*
现代数学的著名证明之一是 Georg Cantor 证明了有理数是可枚举的。他是用下面这一张表来证明这一命题的：
1/1 1/2 1/3 1/4 1/5 ...
2/1 2/2 2/3 2/4 ...
3/1 3/2 3/3 ...
4/1 4/2 ... 
5/1 ...
我们以 Z 字形给上表的每一项编号。第一项是 1/1，然后是 1/2，2/1，3/1，2/2，……。
输入格式
输入一个整数 N（1≤N≤10^7）。
输出格式
输出表中的第 N 项。
*/
#include <stdio.h>
int main(){
    int N,n;
    scanf("%d",&N);
    /*n(n+1)/2 <= N  <= (n+1)(n+2)/2
      n(n+1)   <= 2N <= (n+1)(n+2)
    */
    for (n=0;n<=4473;n++){
        if (n*(n+1)<=2*N&&2*N<=(n+1)*(n+2)){
        break;
        }
    }
   /*n为偶数时N - n(n+1)/2 作分母,n为奇数时,作分子
    n+2=分子加分母      */
    if (n%2==0){
        printf("%d/%d",n+2-(N-n*(n+1)/2),N-n*(n+1)/2);
    }
    else {
        printf("%d/%d",N-n*(n+1)/2,n+2-(N-n*(n+1)/2));
    }
}
/*另一种累计斜线长度定位,避免了"magic number" 4473
int main(){
    int N;
    scanf("%d", &N);
    int line = 1,sum = 1;
    while (sum<N){
        line++;
        sum+=line;
    }
    int pos=N-(sum-line);
    if (line%2==0){
        printf("%d/%d",pos,line-pos+1);
    }
    else{
        printf("%d/%d",line-pos+1,pos);
    }
    return 0;
}
*/