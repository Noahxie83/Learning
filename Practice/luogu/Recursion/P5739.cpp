/*
求 n!，也就是 1×2×3⋯×n。
挑战：尝试不使用循环语句（for、while）完成这个任务。
输入格式
第一行输入一个正整数 n。
输出格式
输出一个正整数，表示 n!。
*/
#include <iostream>
#include <vector>
using namespace std;
long long jiecheng(long long n);
vector<long long> saved;
int main(){
    long long n;
    cin>>n;
    saved.resize(n+1);
    cout<<jiecheng(n);
    return 0;
}
long long jiecheng(long long n){
    if (n<2){
        return 1;
    }
    if (saved[n]!=0){
        return saved[n];
    }
    saved[n]=n*jiecheng(n-1);
    return saved[n];
}