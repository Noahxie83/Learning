/*
小明的花店新开张，为了吸引顾客，他想在花店的门口摆上一排花，共 m 盆。
通过调查顾客的喜好，小明列出了顾客最喜欢的 n 种花，从 1 到 n 标号。
为了在门口展出更多种花，规定第 i 种花不能超过 a_i盆，摆花时同一种花放在一起，且不同种类的花需按标号的从小到大的顺序依次摆列。
试编程计算，一共有多少种不同的摆花方案。
输入格式
第一行包含两个正整数 n 和 m，中间用一个空格隔开。
第二行有 n 个整数，每两个整数之间用一个空格隔开，依次表示 a_1,a_2,⋯,a_n。
输出格式
一个整数，表示有多少种方案。注意：因为方案数可能很多，请输出方案数对 10^6+7 取模的结果。
*/
#include <iostream>
#include <vector>
#include <algorithm>
#define MOD 1000007
using namespace std;
int main(){
    int n,m;
    cin>>n>>m;
    vector<int> a(n+1,0);
    for (int i=1;i<=n;i++) cin>>a[i];
    vector<vector<int>> dp(n+1,vector<int> (m+1,0));
    dp[0][0]=1;
    for (int i=1;i<=n;i++) //枚举花的种类
        for (int j=0;j<=m;j++) //枚举当前摆的总数
            for (int k=0;k<=min(j,a[i]);k++) dp[i][j]=(dp[i][j]+dp[i-1][j-k])%MOD;//动态规划当前花放多少盆
    cout<<dp[n][m]<<endl;
    return 0;
}