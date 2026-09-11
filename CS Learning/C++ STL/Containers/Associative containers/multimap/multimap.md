# multimap — 允许重复键的有序映射

[查看源码](./multimap.cpp) · [返回 C++ STL 笔记目录](../../../README.md)

本文按原文件中的注释整理，保留原始学习记录；文末附完整源码。

## 学习笔记

multimap容器里的元素,都是pair形式的

```cpp
    multimap<T1,T2> mp;
```

则mp里的元素都是如下类型:

```cpp
struct {
    T1 first;//关键字
    T2 second;//值
};
```

multimap中的元素按照first排序,并可以按first进行查找

缺省的排序规则是"a.first&lt;b.first"为true,则a排在b前面

## 行内与短注释

行号对应同目录中的原源码，保留注释与代码位置的对应关系。

| 源码行号 | 对应代码 | 原注释 |
| --- | --- | --- |
| 13 | ` #include <map> ` | 使用multimap和map需要包含此头文件 |
| 25 | 独立注释 | 此后MAP\_STD等价于multimap&lt;int, StudentInfo&gt; |
| 26 | 独立注释 | typedef int\*PINT; |
| 27 | 独立注释 | 则此后PINT等价于int\*.即PINT p;等价于 int\*p; |
| 36 | ` } ` | make\_pair生成一个pair&lt;int,StudentInfo&gt;变量 |
| 37 | 独立注释 | 其first等于st.score,second等于st.info |
| 44 | ` score=p->first; ` | 比要查询分数低的最高分 |
| 47 | ` for(;p!=mp.begin()&&p->first==score;p--){ ` | 遍历所有成绩和score相等的学生 |
| 53 | ` if(p->first==score){ ` | 如果上面循环是因为p==mp.begin()而终止,则p指向的元素还要处理 |
| 61 | 独立注释 | lower\_bound的结果就是begin,说明没人分数比查询分数低 |

## 完整源码

```cpp
/*
multimap容器里的元素,都是pair形式的
    multimap<T1,T2> mp;
则mp里的元素都是如下类型:
struct {
    T1 first;//关键字
    T2 second;//值
};
multimap中的元素按照first排序,并可以按first进行查找
缺省的排序规则是"a.first<b.first"为true,则a排在b前面
*/
#include <iostream>
#include <map>//使用multimap和map需要包含此头文件
#include <cstring>
using namespace std;
struct StudentInfo {
    int id;
    char name [20];
};
struct Student {
    int score;
    StudentInfo info;
};
typedef multimap<int,StudentInfo> MAP_STD;
// 此后MAP_STD等价于multimap<int, StudentInfo>
// typedef int*PINT;
// 则此后PINT等价于int*.即PINT p;等价于 int*p;
int main (){
    MAP_STD mp;
    Student st;
    char cmd[20];
    while(cin>>cmd){
        if(cmd[0]=='A'){
            cin>>st.info.name>>st.info.id>>st.score;
            mp.insert(make_pair(st.score,st.info));
        } //make_pair生成一个pair<int,StudentInfo>变量
          //其first等于st.score,second等于st.info
        else if(cmd[0]=='Q'){
            int score;
            cin>>score;
            MAP_STD::iterator p=mp.lower_bound(score);
            if (p!=mp.begin()){
                p--;
                score=p->first;//比要查询分数低的最高分
                MAP_STD::iterator maxp=p;
                int maxID=p->second.id;
                for(;p!=mp.begin()&&p->first==score;p--){//遍历所有成绩和score相等的学生
                    if (p->second.id>maxID){
                        maxp=p;
                        maxID=p->second.id;
                    }
                }
                if(p->first==score){//如果上面循环是因为p==mp.begin()而终止,则p指向的元素还要处理
                    if (p->second.id>maxID){
                        maxp=p;
                        maxID=p->second.id;
                    }
                }
                cout<<maxp->second.name<<" "<<maxp->second.id<<" "<<maxp->first<<endl;
            }
            //lower_bound的结果就是begin,说明没人分数比查询分数低
            else cout<<"Nobody"<<endl;
        }
    }
    return 0;
}
```
