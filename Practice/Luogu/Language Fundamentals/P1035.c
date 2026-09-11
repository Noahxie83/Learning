/*
题目描述
已知:S_n= 1+1/2+1/3+...+1/n。显然对于任意一个整数k,当n足够大的时候,S_n>k。
现给出一个整数k,要求计算出一个最小的n,使得S_n>k。
输入格式
一个正整数k。
输出格式
一个正整数n。
*/
#include <stdio.h>
int main(){
    int k,n=1;
    double sum=0;
    scanf("%d",&k);
    while (sum<=k){
        sum+=1.0/n;
        n++;
    }
    printf("%d",n-1);
    return 0;
}