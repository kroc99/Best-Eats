#include <iostream>
#include <cstdlib>
#include <vector>

using namespace std;

// swamp_maze is the 2D grid of the swamp with coffee beans at each location
int swampExplorer(vector<vector<int>> &swamp_maze){

    // if maze empty, return 0
    if (swamp_maze.empty() and swamp_maze[0].empty()){
        return 0;
    }

    // set m as cols and n as rows
    int m = swamp_maze.size();
    int n = swamp_maze[0].size();

    // create temp 2d grid
    vector<vector<int>> temp(m, vector<int>(n,0));

    // start at col 0, row 0
    temp[0][0] = swamp_maze[0][0];

    // fill in temp's first col
    for (int i = 1; i < m; ++i){
        temp[i][0] = temp[i-1][0] + swamp_maze[i][0];
    }

    // fill in the temp's first row
    for (int j = 1; j < n; ++j){
        temp[0][j] = temp[0][j-1] + swamp_maze[0][j];
    }

    // determine max beans for each cell
    for (int i = 1; i < m; ++i) {
        for (int j = 1; j < n; ++j){
            temp[i][j] = max(temp[i-1][j], temp[i][j-1]) + swamp_maze[i][j];
        }
    }

    // bottom right will have max beans
    int max_beans = temp[m-1][n-1];

    // return the max beans that alberta can collect
    return max_beans;

}