/*
已知n个整数 x_1,x_2,⋯,x_n，以及1个整数 k（k<n）。从n个整数中任选k个整数相加，可分别得到一系列的和。
例如当n=4，k=3，4个整数分别为3,7,12,19 时，可得全部的组合与它们的和为：
3+7+12=22
3+7+19=29
7+12+19=38
3+12+19=34
现在，要求你计算出和为素数共有多少种。
例如上例，只有一种的和为素数：3+7+19=29。
输入格式
第一行两个空格隔开的整数 n,k（1≤n≤20，k<n）。
第二行n个整数，分别为x_1,x_2,⋯,x_n（1≤x_i≤5×10^6）。
输出格式
输出一个整数，表示种类数。
*/
#include <iostream>
using namespace std;
bool isPrime(int n);
void choose(int start,int selected,int sum);
int n,k,a[20],cnt=0;
int main(){
    cin>>n>>k;
    for (int i=0;i<n;i++){
        cin>>a[i];
    }
    choose(0,0,0);
    cout<<cnt;
    return 0;
}
bool isPrime(int n){
    for (int i=2;i*i<=n;i++){
        if (n<2){
            return false;
        }
        if (n%i==0){
            return false;
        }
    }
    return true;
}
void choose(int start,int selected,int sum){
    if (selected==k){
        if(isPrime(sum)){
            cnt++;
        }
        return;
    }
    for (int i=start;i<n;i++){
        choose(i+1,selected+1,sum+a[i]);
    }
}