/*
给定只由 6 种括号字符组成的字符串：(, ), [, ], {, }。判断每个字符串是否为“合法括号序列”，合法则输出 YES，否则输出 NO。合法括号序列的定义：
空串合法；
若 A 合法，则 (A), [A], {A} 均合法；
若 A 与 B 均合法，则 AB 合法。
输入格式
第一行一个整数 T，表示数据组数。接下来 T 行，每行一个只包含上述 6 种字符的字符串。
输出格式
对于每个字符串，输出一行：
若其为合法括号序列，输出 YES；
否则输出 NO。
*/
#include <iostream>
#include <string>
#include <stack>
using namespace std;
bool check(string s);
int main(){
    int T;
    cin>>T;
    while(T--){
        string s;
        cin>>s;
        if(check(s)){
            cout<<"YES"<<endl;
        }
        else{
            cout<<"NO"<<endl;
        }
    }
    return 0;
}
bool check(string s){
    stack<char> str;
    for (char c:s){
        if (c=='('||c=='['||c=='{'){//左括号入栈
            str.push(c);
        } 
        else{
            if (str.empty()){
                return false;
            }
            char top=str.top();
            if((c==')'&&top!='(')||(c==']'&&top!='[')||(c=='}'&&top!='{')){//匹配右括号，要与栈顶一一对应
                return false;
            }
            str.pop();
        }
    }
    return str.empty();
}