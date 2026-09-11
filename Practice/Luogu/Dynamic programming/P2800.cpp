/*
小 A 在玩《剑仙》，他遇到了一个锁妖塔，想从外面爬上去。
锁妖塔共有 n 层，第 i 层的高度为 h_i。小 A 初始时在地面上，他爬上第 i 层需要花费的时间等于该层高度 h_i。
小 A 会用仙术，每用一次可以让他向上跳一层或两层，该过程不花费时间。
但是每次跳跃后小 A 都将用完力气，必须再爬过至少一层休息才可以继续使用仙术跳跃。
现在小 A 想让你帮他算出爬上塔顶（第 n 层）的最短时间。
输入格式
第一行一个整数 n 表示锁妖塔的层数。
第二行 n 个整数 h_i
表示从下往上第 i 层的高度。
输出格式
一行一个整数 t，表示最短时间。
*/
#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;
int main(){
	int n;
	cin>>n;
	vector<int> h(n+2,0),dp(n+2,0);
	for (int i=1;i<=n;i++)cin>>h[i];
	// dp[i]=min(dp[i-1],dp[i-2],dp[i-3])+h[i]
	// 注意要算到n+1层
    for (int i=1;i<=n+1;i++){
    	dp[i]=dp[i-1]+h[i];
    	if(i-2>=0) dp[i]=min(dp[i],dp[i-2]+h[i]);
    	if(i-3>=0) dp[i]=min(dp[i],dp[i-3]+h[i]);
    }
	cout<<dp[n+1]<<endl;
	return 0;
}
