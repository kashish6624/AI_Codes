#include <iostream>
#include <cmath>
#include <vector>
#include <chrono>
using namespace std;

bool Place(int k, int i, int X[]){
    for(int j=0;j<k;j++){
        if(X[j] == i || (abs(X[j]-i) == abs(j-k))){
            return false;
        }
    }
    return true;
}

void Nqueens(int k, int n, int X[], vector<vector<int>>& solutions, int& count){
    for(int i=0;i<n;i++){
        if(Place(k, i, X)){
            X[k] = i;
            if(k == n-1){ // Check if all queens are placed
                vector<int> solution;
                for(int j=0;j<n;j++){
                    solution.push_back(X[j] + 1); // Storing positions in a solution vector
                }
                solutions.push_back(solution); // Storing the solution set
                count++;
            }
            else{
                Nqueens(k+1, n, X, solutions, count);
            }
        }
    }
}

int main(){
    int n;

    cout << "Enter number of queens to be placed:";
    cin >> n;

    int X[n];
    vector<vector<int>> solutions;
    int count = 0;

    auto start = chrono::high_resolution_clock::now();

    Nqueens(0, n, X, solutions, count);

    // Print all the solutions
    for(const auto& solution : solutions){
        for(int pos : solution){
            cout << pos << " ";
        }
        cout << endl;
    }

    cout << "Number of queens: " << n << endl;
    cout << "Number of solutions: " << count << endl;

    auto end = chrono::high_resolution_clock::now();
    chrono::duration<float> duration = end - start;

    cout << "Time taken is: " << duration.count() << " seconds" << endl;

    return 0;
}