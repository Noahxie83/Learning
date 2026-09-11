/*
一般的文本编辑器都有查找单词的功能，该功能可以快速定位特定单词在文章中的位置，有的还能统计出特定单词在文章中出现的次数。
现在，请你编程实现这一功能，具体要求是：给定一个单词，请你输出它在给定的文章中出现的次数和第一次出现的位置。
注意：匹配单词时，不区分大小写，但要求完全匹配，即给定单词必须与文章中的某一独立单词在不区分大小写的情况下完全相同（参见样例 1），
如果给定单词仅是文章中某一单词的一部分则不算匹配（参见样例 2）。
输入格式
共 2 行。
第 1 行为一个字符串，其中只含字母，表示给定单词；
第 2 行为一个字符串，其中只可能包含字母和空格，表示给定的文章。
输出格式
一行，如果在文章中找到给定单词则输出两个整数，两个整数之间用一个空格隔开，分别是单词在文章中出现的次数和第一次出现的位置
（即在文章中第一次出现时，单词首字母在文章中的位置，位置从 0 开始）；如果单词在文章中没有出现，则直接输出一个整数 −1。
注意：空格占一个字母位。
*/
#include <iostream>
#include <string>
using namespace std;
int main(){
    string w,p;
    int cnt=0,flag=0;
    getline(cin,w);
    getline(cin,p);
    for (int i=0;i<w.size();i++){
        if (w[i]<'a'){
            w[i]+='a'-'A';
        }
    }
    for (int i=0;i<p.size();i++){
        if (p[i]>='A'&&p[i]<='Z'){
            p[i]+='a'-'A';
        }
    }
    for (int i=0;i<p.size();i++){
        if (p[i]==' '){
            continue;
        }
        int w_len=0,j=i;
        while (j<p.size()&&p[j]!=' '){
            w_len++;
            j++;
        }
        if (w_len==w.size()){
            int same=1;//初始化为same
            for (int k=0;k<w_len;k++){
                if (p[i+k]!=w[k]){
                    same=0;
                    break;
                }
            }
            if (same){
                if (cnt==0){
                    flag=i;
                }
                cnt++;
            }
        }
        i=j;//跳过检查过的单词
    }
    if (cnt>0){
        cout<<cnt<<' '<<flag<<endl;
    }else {
        cout<<-1<<endl;
    }
    return 0;
}