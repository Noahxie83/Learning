/*
写一个程序来查找从最高点到底部任意处结束的路径，使路径经过数字的和最大。每一步可以走到左下方的点也可以到达右下方的点。
输入格式
第一个行一个正整数 r，表示行的数目。
后面每行为这个数字金字塔特定行包含的整数。
输出格式
单独的一行，包含那个可能得到的最大的和。
*/
#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;
int main(){
    int r;
    cin>>r;
    vector<vector<int>> a(r,vector<int> (r,0));
    for (int i=0;i<r;i++){
        for (int j=0;j<=i;j++) cin>>a[i][j];
    }
    vector<int> dp(r,0);
    dp[0]=a[0][0];
    //newdp[j]=min(dp[j],dp[j-1])+a[i][j]
    //newdp[0]=dp[0]+a[i][0];
    //newdp[i]=dp[i-1]+a[i][i];
    for (int i=1;i<r;i++){
        vector<int> newdp(r,0);
        newdp[0]=dp[0]+a[i][0];
        for(int j=1;j<i;j++)newdp[j]=max(dp[j-1],dp[j])+a[i][j];
        newdp[i]=dp[i-1]+a[i][i];
        dp=newdp;
    }
    cout<<*max_element(dp.begin(),dp.end());
    return 0;
}