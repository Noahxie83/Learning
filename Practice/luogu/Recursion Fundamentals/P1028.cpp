/*
给出正整数 n，要求按如下方式构造数列：
只有一个数 n 的数列是一个合法的数列。
在一个合法的数列的末尾加入一个正整数，但是这个正整数不能超过该数列最后一项的一半，可以得到一个新的合法数列。
请你求出，一共有多少个合法的数列。两个合法数列 a,b 不同当且仅当两数列长度不同或存在一个正整数i≤|a|，使得 a_i!=b_i。
输入格式
输入只有一行一个整数，表示 n。
输出格式
输出一行一个整数，表示合法的数列个数。
*/
#include <iostream>
using namespace std;
int count(int n);
int main(){
    int n;
    cin>>n;
    cout<<count(n);
    return 0;
}
int count(int n){
    int cnt=1;
    for (int i=1;i<=n/2;i++)
        cnt+=count(i);
    return cnt;
}
//时间复杂度大,容易超时,以下优化函数(记忆化递归方案):
/*
int a[1001](全局变量)
int count(int n){
    if(a[n]!=0){
        return a[n];
        }
    int cnt=1;
    for(int i=1;i<=n/2;i++){
        cnt+=count(i);
    }
    a[n]=cnt;
    return cnt;
}
*/