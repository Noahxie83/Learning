/*
在日常生活中，通过年、月、日这三个要素可以表示出一个唯一确定的日期。
牛牛习惯用 8 位数字表示一个日期，其中，前 4 位代表年份，接下来 2 位代表月份，最后 2 位代表日期。显然：一个日期只有一种表示方法，而两个不同的日期的表示方法不会相同。
牛牛认为，一个日期是回文的，当且仅当表示这个日期的 8 位数字是回文的。现在，牛牛想知道：在他指定的两个日期之间（包含这两个日期本身），有多少个真实存在的日期是回文的。
一个 8 位数字是回文的，当且仅当对于所有的 i（1≤i≤8）从左向右数的第 i 个数字和第 9−i 个数字（即从右向左数的第 i 个数字）是相同的。
例如：
对于 2016 年 11 月 19 日，用 8 位数字 20161119 表示，它不是回文的。
对于 2010 年 01 月 02 日，用 8 位数字 20100102 表示，它是回文的。
对于 2010 年 10 月 02 日，用 8 位数字 20101002 表示，它不是回文的。
每一年中都有 12 个月份：
其中，1,3,5,7,8,10,12 月每个月有 31 天；4,6,9,11 月每个月有 30 天；而对于 2 月，闰年时有 29 天，平年时有 28 天。
一个年份是闰年当且仅当它满足下列两种情况其中的一种：
这个年份是 4 的整数倍，但不是 100 的整数倍；
这个年份是 400 的整数倍。
例如：
以下几个年份都是闰年：2000,2012,2016。
以下几个年份是平年：1900,2011,2014。
输入格式
两行，每行包括一个 8 位数字。
第一行表示牛牛指定的起始日期。
第二行表示牛牛指定的终止日期。
保证 date_1和 date_2都是真实存在的日期，且年份部分一定为 4 位数字，且首位数字不为 0。
保证 date_1一定不晚于 date_2。
输出格式
一个整数，表示在date_1和date_2之间，有多少个日期是回文的。
*/
#include <iostream>
#include <string>
using namespace std;
int year(string d);
bool huiwen(string d);
bool runnian(int y);
int main(){
    int mon[13]={0,31,28,31,30,31,30,31,31,30,31,30,31};
    string d1,d2;
    cin>>d1>>d2;
    int y1=year(d1),y2=year(d2),date1=stoi(d1),date2=stoi(d2),cnt=0;
    for (int y=y1;y<=y2;y++){
        for (int m=1;m<=12;m++){
            int days=mon[m];
            if (m==2 && runnian(y)){
                days++;
            }
            for (int d=1;d<=days;d++){
                int date=y*10000+m*100+d;
                if (date<date1||date>date2){
                    continue;
                }
                string s=to_string(date);
                if (huiwen(s)){
                    cnt++;
                }
            }
        }
    }
    cout<<cnt<<endl;
    return 0;
}
int year(string d){
    int y=(d[0]-'0')*1000+(d[1]-'0')*100+(d[2]-'0')*10+(d[3]-'0');
    return y;
}
bool huiwen(string d){
    for (int i=0;i<4;i++){
        if (d[i]!=d[7-i]){
            return false;
        }
    }
    return true;
}
bool runnian(int y){
    if (y%4==0&&y%100!=0||y%400==0){
        return true;
    }
    else {
        return false;
    }
}