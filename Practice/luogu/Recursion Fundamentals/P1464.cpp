/*
对于一个递归函数 w(a,b,c)
如果 a≤0 或 b≤0 或 c≤0 就返回值 1。
如果 a>20 或 b>20 或 c>20 就返回 w(20,20,20)
如果 a<b 并且 b<c 就返回 w(a,b,c−1)+w(a,b−1,c−1)−w(a,b−1,c)。
其它的情况就返回 w(a−1,b,c)+w(a−1,b−1,c)+w(a−1,b,c−1)−w(a−1,b−1,c−1)
这是个简单的递归函数，但实现起来可能会有些问题。当 a,b,c 均为 15 时，调用的次数将非常的多。你要想个办法才行。
注意：例如 w(30,−1,0) 又满足条件 1 又满足条件 2，请按照最上面的条件来算，答案为 1。
输入格式
会有若干行。
并以 −1,−1,−1 结束。
输出格式
输出若干行，每一行格式：
w(a, b, c) = ans
注意空格。
保证输入的数在 [−9223372036854775808,9223372036854775807] 之间，并且是整数。
保证不包括 −1,−1,−1 的输入行数 T 满足1≤T≤10^5 
*/
#include <iostream>
#define MAX 10000
using namespace std;
long long w(long long a,long long b,long long c);
long long saved[21][21][21];
int main(){
    long long a,b,c;
    while(cin>>a>>b>>c){
        if (a==-1&&b==-1&&c==-1){
            break;
        }
        cout<<"w("<<a<<", "<<b<<", "<<c<<") = "<<w(a,b,c)<<endl;
    }
    return 0;
}
long long w(long long a,long long b,long long c){
    if (a<=0||b<=0||c<=0){
        return 1;
    }
    else if (a>20||b>20||c>20){
        return w(20,20,20);
    }
    if (saved[a][b][c]!=0){
        return saved[a][b][c];
    }
    if (a<b&&b<c){
        saved[a][b][c]=w(a,b,c-1)+w(a,b-1,c-1)-w(a,b-1,c);
    }
    else {
        saved[a][b][c]=w(a-1,b,c)+w(a-1,b-1,c)+w(a-1,b,c-1)-w(a-1,b-1,c-1);
    }
    return saved[a][b][c];
}