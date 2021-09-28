#include <iostream>
#include<algorithm>
#include <vector>
#include <utility>
#include <cstring> 
const int N = 1005;
using namespace std;
typedef pair<int,int> pr;

int main(){
	vector<pr> a,b;
	int n,l,c,rs=0;
	int t,d[2*N][2*N] = {0};
	
	cin >> n;
	for(int k = 0; k < n; k++){
		cin >> l >> c;
		for(int i = 0; i < l; i++){
			for(int j = 0; j < c; j++){
				cin >> t;
				if(t == 1){
				    a.push_back(pr(i,j));
				}
			}
		}
		for(int i = 0; i < l; i++){
			for(int j = 0; j < c; j++){
				cin >> t;
				if(t == 1){
				    b.push_back(pr(i,j));
				}
			}
		}
	    for(int i = 0; i < a.size(); i++){
		    for(int j = 0; j < b.size(); j++){
			    rs = max(rs,++d[a[i].first - b[j].first + N][a[i].second - b[j].second + N]);
	    	}
    	}
    	cout << rs <<endl;
    	rs=0;
    	a.clear();
    	b.clear();
        memset(d, 0, sizeof(d)); 
	}	
	return 0;
}