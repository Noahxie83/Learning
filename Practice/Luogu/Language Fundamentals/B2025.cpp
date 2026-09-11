/*
用 * 构造一个对角线长 5 个字符，倾斜放置的菱形。
*/
#include <iostream>
#include <string>
using namespace std;
int main(){
    string s="*";
    cout<<"  "<<s<<endl;
    cout<<" "<<s+s+s<<endl;
    cout<<s+s+s+s+s<<endl;
    cout<<" "<<s+s+s<<endl;
    cout<<"  "<<s<<endl;
    return 0;
}