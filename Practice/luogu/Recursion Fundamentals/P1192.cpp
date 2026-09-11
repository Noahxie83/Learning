/*
有N级台阶，你一开始在底部，每次可以向上迈1∼K级台阶，问到达第N级台阶有多少种不同方式。
输入格式
两个正整数 N,K。
输出格式
一个正整数 ans(mod100003)，为到达第 N 级台阶的不同方式数。
*/
#include <iostream>
using namespace std;
long long saved[100000]={0};
long long bushu(int N,int K);
int main(){
    int N,K;
    cin>>N>>K;
    cout<<bushu(N,K)<<endl;
    return 0;
}
long long bushu(int N,int K){
    if (N==0){
        return 1;
    }
    if (N<0){//防止走过头
        return 0;
    }
    if (saved[N]!=0){
        return saved[N];
    }
    for (int i=1;i<=K;i++){
        saved[N]+=bushu(N-i,K);
        saved[N]%=100003;
    }
    return saved[N];
}