/*
R 君在练习打字。有这样一个打字练习网站，给定一个范文和输入框，会根据你的输入计算准确率和打字速度。
可以输入的字符有小写字母、空格、<（退格键，解释见后）和 .（英文句号），输入字符后，光标也会跟着移动。
输入的文本有多行，R 君可以通过换行键来换行，换行后光标移动到下一行的开头。
R 君可以按退格键（范文也可以），以删除上一个打的字符，并将光标回移一格。特殊的，如果此时光标已经在一行的开头，则不能继续退格（即忽略此时输入的退格键）。
网站的比较方式遵循以下两个原则：
逐行比较，即对于范文和输入的每一行依次比较，不同行之间不会产生影响，多余有打字符的行会被忽略。
逐位比较，即对于两行的每一个字符依次比较，当且仅当字符相同时才会被算作一次正确，否则会被算作错误。计算答案时，只统计相同的字符个数。
需要注意的是，回车键不会被计入正确的字符个数。
R 君看到网站上显示他花了 T 秒完成了这次的打字游戏，请你计算出他的 KPM（Keys per minutes，每分钟输入的字符个数），答案四舍五入保留整数部分。
输入格式
R 君会依次告诉你网站的范文，他的输入和花费的时间。
其中范文和输入将会这样读入：给定若干行字符串，以单独的一行 EOF 结束，其中 EOF 不算入输入的文本。
最后一行一个整数 T，表示他打字花费了 T 秒。
可以参考样例输入输出文件和样例解释辅助理解。
输出格式
一行一个整数，表示 KPM。
*/
#include <iostream>
#include <string>
#define MAX 10000
using namespace std;
string deal(string s);
int main(){
    int T,w_cnt=0,r_cnt=0;
    string W[MAX],R[MAX];
    while(getline(cin,W[w_cnt])){
        if(W[w_cnt]=="EOF")
            break;
        w_cnt++;
    }
    while(getline(cin,R[r_cnt])){
        if(R[r_cnt]=="EOF")
            break;
        r_cnt++;
    }
    cin>>T;
    for(int i=0;i<w_cnt;i++){
        W[i]=deal(W[i]);
    }//处理范文的退格
    for(int i=0;i<r_cnt;i++){
        R[i]=deal(R[i]);
    }//处理R的退格
    int cnt=0;
    for(int i=0;i<w_cnt&&i<r_cnt;i++){
        int len=min(W[i].size(),R[i].size());
        for(int j=0;j<len;j++){
            if(W[i][j]==R[i][j]){
                cnt++;
            }
        }
    }
    cout<<cnt*60/T<<endl;
    return 0;
}
string deal(string s){
    char ret[100000];
    int len=0;
    for(int i=0;i<s.size();i++){
        if(s[i]=='<'){
            if(len>0){
                len--;
            }
        }
        else{
            ret[len]=s[i];
            len++;
        }
    }
    string ans="";
    for(int i=0;i<len;i++){
        ans+=ret[i];
    }
    return ans;
}//处理退格