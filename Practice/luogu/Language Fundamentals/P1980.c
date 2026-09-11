/*
题目描述
试计算在区间 1 到 n 的所有整数中，数字 x（0≤x≤9）共出现了多少次？
例如，在 1 到 11 中，即在 1,2,3,4,5,6,7,8,9,10,11 中，数字 1 出现了 4 次。
输入格式
2 个整数 n,x，之间用一个空格隔开。
输出格式
1 个整数，表示 x 出现的次数。
*/
#include <stdio.h>
//int weishu(int i);
int main(){
    int n,x,cnt=0;
    scanf("%d %d",&n,&x);
    for (int i=1;i<=n;i++){
        /*int m=weishu(i),tmp=i;
        while (m>0){
            tmp%=m;
            m/=10;
            if (tmp/m==x){
                cnt++;
            }
        }*/
        int tmp=i;
        while (tmp>0){
            if (tmp%10==x){
                cnt++;
            }
            tmp/=10;
        }
    }
    printf("%d",cnt);
    return 0;
}
/*int weishu(int i){
    int m=1;
    while(i>9){
        i/=10;
        m*=10;
    }
    return m;
}//事实上本题不需要取每一位
//这里的weishu函数是从最低位取的案例*/