/*
将整数 n 分成 k 份，且每份不能为空，任意两个方案不相同（不考虑顺序）。
例如：n=7，k=3，下面三种分法被认为是相同的。
1,1,5；
1,5,1；
5,1,1。
问有多少种不同的分法。
输入格式
n,k（6<n≤200,2≤k≤6）。
输出格式
1个整数，即不同的分法。
*/
#include <iostream>
using namespace std;
int fenfa(int n,int k,int min);
int main(){
    int n,k;
    cin>>n>>k;
    cout<<fenfa(n,k,1)<<endl;
    return 0;
}
int fenfa(int n,int k,int min){//把每一次走的都要记录保证是从小到大的顺序
    if(k==1){
        if(n>=min){
            return 1;
        }
        return 0;
    }
    int cnt=0;
    for(int i=min;i<=n/k;i++){
        cnt+=fenfa(n-i,k-1,i);
    }
    return cnt;
}