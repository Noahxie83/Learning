/*
小 A 最近一直在找自己的爸爸，用什么办法呢，就是 DNA 比对。
小 A 有一套自己的 DNA 序列比较方法，其最终目标是最大化两个 DNA 序列的相似程度，具体步骤如下：
给出两个 DNA 序列，第一个长度为 n，第二个长度为 m。
在两个序列的任意位置插入任意多的空格，使得两个字符串长度相同
逐位进行匹配，如果两个序列相同位置上的字符都不是空格，假设第一个是 x，第二个是 y，那么他们的相似程度由 d(x,y) 定义。
对于两个序列中任意一段极长的长度为 k 的连续空格，我们定义这段空格的相似程度为 g(k)=−A−B(k−1)。
那么最终两个序列的相似程度就是所有的 d(x,y) 加上所有的极长空格段的相似程度之和。
现在小 A 通过某种奥妙重重的方式得到了小 B 的 DNA 序列中的一段，他想请你帮他算一下小 A 的 DNA 序列和小 B 的 DNA 序列的最大相似程度。
输入格式
输入第 1 行一个字符串，表示小 A 的 DNA 序列。
输入第 2 行一个字符串，表示小 B 的 DNA 序列。
接下来 4 行，每行 4 个整数，用空格隔开，表示 d 数组，具体顺序如下所示。
d(A,A) d(A,T) d(A,G) d(A,C)
d(T,A) d(T,T) d(T,G) d(T,C)
d(G,A) d(G,T) d(G,G) d(G,C)
d(C,A) d(C,T) d(C,G) d(C,C)
最后一行两个用空格隔开的正整数 A,B，意义如题中所述。
输出格式
输出共一行，表示两个序列的最大相似程度。
*/
#include <iostream>
#include <vector>
#include <array>
#include <algorithm>
#include <string>
using namespace std;
// dp[i][j][flag] s_i、t_j
// flag==0表示无空格,flag=1表示空格在s,flag=2表示空格在t
// dp[i][j][0]=max(dp[i-1][j-1][0],dp[i-1][j-1][1],dp[i-1][j-1][2])+d(s[i],t[j])
// dp[i][j][1]=max(dp[i][j-1][0]-A,dp[i][j-1][1]-B,dp[i][j-1][2]-A)
// dp[i][j][2]=max(dp[i-1][j][0]-A,dp[i-1][j][1]-A,dp[i-1][j][2]-B)
const int NEG=-1e9;// 设置成极小值
int getId(char c){
    if (c=='A') return 0;
    if (c=='T') return 1;
    if (c=='G') return 2;
    return 3;  // C
}
int main(){
    string s,t;
    cin>>s>>t;
    int n=s.size(),m=t.size(),d[4][4],A,B;
    for (int i=0;i<4;i++)
        for (int j=0;j<4;j++) 
            cin>>d[i][j];
    cin>>A>>B;
    vector<vector<array<int,3>>> dp(n+1,vector<array<int,3>>(m+1,{NEG,NEG,NEG}));
    dp[0][0][0]=0;
    for (int j=1;j<=m;j++)dp[0][j][1]=-A-B*(j-1);
    for (int i=1;i<=n;i++)dp[i][0][2]=-A-B*(i-1);
    for (int i=1;i<=n;i++){
        for (int j=1;j<=m;j++){
            int x=getId(s[i-1]),y=getId(t[j-1]);
            dp[i][j][0]=max({dp[i-1][j-1][0],dp[i-1][j-1][1],dp[i-1][j-1][2]})+d[x][y];
            dp[i][j][1]=max({dp[i][j-1][0]-A,dp[i][j-1][1]-B,dp[i][j-1][2]-A});
            dp[i][j][2]=max({dp[i-1][j][0]-A,dp[i-1][j][1]-A,dp[i-1][j][2]-B});
        }
    }
    cout<<max({dp[n][m][0],dp[n][m][1],dp[n][m][2]});
    return 0;
}