#include <bits/stdc++.h>
using namespace std;
const int N = 1000005;
int n;
int main(){
    cin >> n;
    while(n != 0){
        unsigned long long a[N], l[N], r[N], D[N], top = 0;;
        for(int i = 1; i <= n; i++)
            cin >> a[i];
        D[0] = 0;
        for(int i = 1; i <= n; i++){
            while(top > 0 && a[D[top]] >= a[i])
                top--;
            l[i] = D[top] + 1;
            D[++top] = i;
        }
        D[0] = n+1; top = 0;
        for(int i = n; i >= 1; i--){
            while(top > 0 && a[D[top]] >= a[i])
                top--;
            r[i] = D[top] - 1;
            D[++top] = i;
        }
        unsigned long long res = 0;
        for(int i = n; i >= 1; i--)
            if(res < a[i]*(r[i]-l[i]+1)){
                res = a[i]*(r[i]-l[i]+1);
            }
        cout << res << endl;
        cin >> n;
    }
    return 0;
}