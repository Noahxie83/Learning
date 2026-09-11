/*
计算两个矩阵的乘法。n×m 阶的矩阵 A 乘以 m×k 阶的矩阵 B 得到的矩阵 C 是 n×k 阶的，
且 C[i][j]=A[i][0]×B[0][j]+A[i][1]×B[1][j]+ …… +A[i][m−1]×B[m−1][j](C[i][j] 表示 C 矩阵中第 i 行第 j 列元素）。
输入格式
第一行为 n,m,k，表示 A 矩阵是 n 行 m 列，B 矩阵是 m 行 k 列，n,m,k 均小于等于 100。
然后先后输入 A 和 B 两个矩阵，A 矩阵 n 行 m 列，B 矩阵 m 行 k 列，矩阵中每个元素的绝对值不会大于 1000。
输出格式
输出矩阵 C，一共 n 行，每行 k 个整数，整数之间以一个空格分开。
*/
#include <iostream>
#include <vector>
using namespace std;
int main(){
    int n,m,k;
    cin>>n>>m>>k;
    vector<vector<int>> A(n,vector<int> (m,0));
    vector<vector<int>> B(m,vector<int> (k,0));
    vector<vector<int>> C(n,vector<int> (k,0));
    for (int i=0;i<n;i++){
        for (int j=0;j<m;j++){
            cin>>A[i][j];
        }
    }
    for (int i=0;i<m;i++){
        for (int j=0;j<k;j++){
            cin>>B[i][j];
        }
    }
    for (int i=0;i<n;i++){
        for (int j=0;j<k;j++){
            for (int t=0;t<m;t++){
                C[i][j]+=A[i][t]*B[t][j];
            }
        }
    }
    for (auto r:C){
        for (auto c:r){
            cout<<c<<" ";
        }
        cout<<endl;
    }
    return 0;
}