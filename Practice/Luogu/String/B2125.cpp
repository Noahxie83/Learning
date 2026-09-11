/*
输入学生的人数，然后再输入每位学生的分数和姓名，求获得最高分数的学生的姓名。
输入格式
第一行输入一个正整数 N（N≤100），表示学生人数。
接着输入 N 行，每行包括一个整数和一个字符串，用空格分开，代表分数姓名。
分数是一个非负整数，且小于等于 100；
姓名为一个连续的字符串，中间没有空格，长度不超过 20。
数据保证所有同学的姓名都不同，而且最高分只有一位同学。
输出格式
获得最高分数同学的姓名。
*/
#include <iostream>
#include <string>
#include <utility>
#include <vector>
using namespace std;
int main(){
    int N;
    cin>>N;
    vector<pair<int,string>> students;
    for(int i=0;i<N;i++){
        int score;
        string name;
        cin>>score>>name;
        students.push_back({score,name});
    }
    int maxScore=-1;
    string ans;
    for(auto s:students){
        if(s.first>maxScore){
            maxScore=s.first;
            ans=s.second;
        }
    }
    cout<<ans;
    return 0;
}