/*
题目描述
X 校正在进行 CSP 前的校内集训。
一共有 n 名 OIer 参与这次集训，教练为他们精心准备了 m 套模拟赛题。
然而，每名 OIer 都有各自的时间安排，巧合的是，他们在接下来的 k 天中都恰好有 m 天有空打模拟赛。
为了方便管理，教练规定一个人必须按顺序打完 m 套模拟赛题。
比如，小 X 在接下来的第 2,3,5 天有空打模拟赛，那么他就必须在第 2 天打第 1 套模拟赛题，第 3 天打第 2 套模拟赛题，第 5 天打第 3 套模拟赛题。
教练需要为每一个人的每一次模拟赛做准备，为了减小工作量，如果在某一天有多个人打同一套模拟赛题，那么教练只需要在这一天准备一场使用这一套题的模拟赛即可。
你作为机房大佬，教练想请你帮他计算一下，他每天需要准备多少场模拟赛。
输入格式
第一行三个整数 n,m,k。
接下来 n 行，每行 m 个整数，第 i 行第 j 列的整数 a_i_j表示第 i 个人在接下来的 k 天中第 j 个有空的日子为第a_i_j天。
输出格式
一行 k 个整数，第 i 个整数表示接下来的第 i 天教练需要准备的模拟赛场数。
*/
#include <iostream>
using namespace std;
int main(){
    int n,m,k,x,peo[1000][1000]={0},day[1000]={0},test[1000][1000]={0};
    cin>>n>>m>>k;
    for (int i=0;i<n;i++){
        for (int j=0;j<m;j++){
            cin>>x;
            peo[i][x-1]=j+1;
        }
    }
    for (int j=0;j<k;j++){
        for (int i=0;i<n;i++){
            int t=peo[i][j];
            if (t!=0&&test[j][t]==0){
                test[j][t]=1;
                day[j]++;                    
            }
        }
    }
/*
6 3 7  
2 3 4  0123000
2 5 7  0100203
3 5 7  0010203
1 3 5  1020300
5 6 7  0000123
1 2 3  1230000

*/
    for(int j=0;j<k;j++){
        if(j!=0) cout << ' ';
        cout << day[j];
    }
    return 0;
}

/*优化题解:
#include <iostream>
using namespace std;
int main(){
    int n,m,k,x;
    bool test[1000][1000]={0};
    int day[1000]={0};
    cin>>n>>m>>k;
    for(int i=0;i<n;i++){
        for(int j=0;j<m;j++){
            cin>>x;
            if(!test[x][j]){           //第x天第j+1套题以前有没有人做过?
                test[x][j]=true;
                day[x]++;
            }
        }
    }
    for (int i=1;i<=k;i++){
        if (i>1){
            cout << ' ';
        }
        cout<<day[i];
    }
    return 0;
}
*/