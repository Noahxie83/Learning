/*
在一个 n×n 的平面上，在每一行中有一条线段，第 i 行的线段的左端点是 (i,L_i)，右端点是 (i,R_i)。
你从 (1,1) 点出发，要求沿途走过所有的线段，最终到达 (n,n) 点，且所走的路程长度要尽量短。
更具体一些说，你在任何时候只能选择向下走一步（行数增加 1）、向左走一步（列数减少 1）或是向右走一步（列数增加 1）。
当然，由于你不能向上行走，因此在从任何一行向下走到另一行的时候，你必须保证已经走完本行的那条线段。
输入格式
第一行有一个整数 n。
以下 n 行，在第 i 行（总第 (i+1) 行）的两个整数表示 L_i和 R_i。
输出格式
仅包含一个整数，你选择的最短路程的长度。
*/
#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;
// dpL[i]=min((dpL[i-1]+abs(L[i-1]-R[i])),(dpR[i-1]+abs(R[i-1]-R[i])))+R[i]-L[i]+1
// dpR[i]=min((dpL[i-1]+abs(L[i-1]-L[i])),(dpR[i-1]+abs(R[i-1]-L[i])))+R[i]-L[i]+1
// 第n行 ans=min((dpL[n]+n-L[i]),(dpR[n]+n-R[i]))
int main(){
    int n;
    cin>>n;
    vector<int> L(n+1,0),R(n+1,0),dpL(n+1,0),dpR(n+1,0);
    for (int i=1;i<=n;i++) cin>>L[i]>>R[i];
    dpL[1]=R[1]+L[1]-1,dpR[1]=R[1]-1;
    for (int i=2;i<=n;i++){
        dpL[i]=min((dpL[i-1]+abs(L[i-1]-R[i])),(dpR[i-1]+abs(R[i-1]-R[i])))+R[i]-L[i]+1;
        dpR[i]=min((dpL[i-1]+abs(L[i-1]-L[i])),(dpR[i-1]+abs(R[i-1]-L[i])))+R[i]-L[i]+1;
    }
    cout<<min((dpL[n]+n-L[n]),(dpR[n]+n-R[n]))<<endl;
    return 0;
}