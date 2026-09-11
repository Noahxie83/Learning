/*
现有 2^n×2^n(n≤10) 名作弊者站成一个正方形方阵等候 kkksc03 的发落。
kkksc03 决定赦免一些作弊者。他将正方形矩阵均分为 4 个更小的正方形矩阵，
每个更小的矩阵的边长是原矩阵的一半。其中左上角那一个矩阵的所有作弊者都将得到赦免，
剩下 3 个小矩阵中，每一个矩阵继续分为 4 个更小的矩阵，然后通过同样的方式赦免作弊者……直到矩阵无法再分下去为止。
所有没有被赦免的作弊者都将被处以棕名处罚。
给出 n，请输出每名作弊者的命运，其中 0 代表被赦免，1 代表不被赦免。
输入格式
一个整数 n。
输出格式
2^n×2^n的 01 矩阵，代表每个人是否被赦免。数字之间有一个空格。
*/
#include <iostream>
#include <vector>
#include <cmath>
using namespace std;
void shemian(vector<vector<int>> &mat,int len,int x,int y);
int main(){
    int n,len;
    cin>>n;
    len=pow(2,n);
    vector<vector<int>> mat(len,vector<int>(len,1));
    shemian(mat,len,0,0);
    for (auto r:mat){
        for (auto c:r){
            cout<<c<<" ";
        }
        cout<<endl;
    }
    return 0;
}
void shemian(vector<vector<int>> &mat,int len,int x,int y){
    if (len==1){
        return;
    }
    int half=len/2;
    //左上
    for(int i=x;i<x+half;i++){
        for(int j=y;j<y+half;j++){
            mat[i][j]=0;
        }
    }
    //右上
    shemian(mat,half,x,y+half);
    //左下
    shemian(mat,half,x+half,y);
    //右下
    shemian(mat,half,x+half,y+half);
}