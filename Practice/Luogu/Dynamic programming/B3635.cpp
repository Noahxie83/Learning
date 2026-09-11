/*
今有面值为 1、5、11 元的硬币各无限枚。
想要凑出 n 元，问需要的最少硬币数量。
输入格式
仅一行，一个正整数 n。
输出格式
仅一行，一个正整数，表示需要的硬币个数。
*/
#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;
int main(){
    long long n;
    cin>>n;
    vector<long long> dp(n+1,0);
    // dp[i]=min(dp[i-1]+dp[i-5]+dp[i-11])+1 (i>5)
    dp[1]=1;
    for (long long i=2;i<=n;i++){
        if (i>10)dp[i]=min(dp[i-1],min(dp[i-5],dp[i-11]))+1;
        else if (i<5)dp[i]=dp[i-1]+1;
        else dp[i]=min(dp[i-1],dp[i-5])+1;
    }
    cout<<dp[n]<<endl;
    return 0;
}