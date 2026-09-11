/*
设有 n 个正整数 a_1…a_n ，请将它们连接成一排，相邻数字首尾相接，组成一个最大的整数。\
输入格式
第一行有一个整数，表示数字个数 n。
第二行有 n 个整数，表示给出的 n 个整数 a_i。
输出格式
一个正整数，表示最大的整数。
*/
/*#include <iostream>
#include <string>
using namespace std;
int weishu(int n);
int main (){
    int n,a[20]={0};
    cin>>n;
    for (int i=0;i<n;i++){
        cin>>a[i];
    }
    char b[20][12]={0};
    for (int i=0;i<n;i++){
        int k=weishu(a[i]),j=0;
        while (k>0){
            b[i][j]=a[i]/k%10+'0';
            j++;
            k/=10;
        }
        b[i][j]='\0';
    }
    for (int i=0;i<n-1;i++){
        for (int j=0;j<n-1;j++){
            string x=b[j],y=b[j+1];
            if(x+y<y+x){
                char temp[12];
                int k=0;
                while(b[j][k]!='\0'){
                    temp[k]=b[j][k];
                    k++;
                }
                temp[k]='\0';
                k=0;
                while(b[j+1][k]!='\0'){
                    b[j][k]=b[j+1][k];
                    k++;
                }
                b[j][k]='\0';
                k=0;
                while(temp[k]!='\0'){
                    b[j+1][k]=temp[k];
                    k++;
                }
                b[j+1][k]='\0';
            }
        }
    }
    for(int i=0;i<n;i++){
        cout<<b[i];
    }
    return 0;
}
int weishu(int n){
    int ret=1;
    while (n>9){
        n/=10;
        ret*=10;
    }
    return ret;
}*/
/*优化题解*/
#include <iostream>
#include <string>
using namespace std;
int main(){
    int n;
    string a[20];
    cin>>n;
    for(int i=0;i<n;i++){
        cin>>a[i];
    }
    for(int i=0;i<n-1;i++){
        for(int j=0;j<n-1-i;j++){
            if(a[j]+a[j+1]<a[j+1]+a[j]){
                swap(a[j],a[j+1]);
            }
        }
    }//冒泡排序法
    for(int i=0;i<n;i++){
        cout<<a[i];
    }
    return 0;
}