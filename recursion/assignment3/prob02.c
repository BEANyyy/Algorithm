//vs에서 돌리면 돌아감.

#include <stdio.h>
#include <stdbool.h>

int N = 8;
int maze[][8] = {
	{0, 0, 0, 0, 0, 0, 0, 1},
	{0, 0, 0, 0, 1, 1, 0, 1},
	{0, 0, 0, 1, 0, 0, 0, 1},
	{0, 0, 0, 0, 1, 1, 0, 0},
	{0, 1, 0, 0, 0, 0, 1, 1},
	{0, 1, 0, 0, 0, 0, 0, 1},
	{0, 0, 0, 1, 0, 0, 0, 1},
	{0, 1, 1, 1, 0, 1, 0, 0}
}; 

/*
{
	{0, 0, 0, 0, 0, 0, 0, 1},
	{ 0, 1, 1, 0, 1, 1, 0, 1 },
	{ 0, 0, 0, 1, 0, 0, 0, 1 },
	{ 0, 1, 0, 0, 1, 1, 0, 0 },
	{ 0, 1, 1, 1, 0, 0, 1, 1 },
	{ 0, 1, 0, 0, 0, 1, 0, 1 },
	{ 0, 0, 0, 1, 0, 0, 0, 1 },
	{ 0, 1, 1, 1, 0, 1, 0, 0 }
};
*/
/* {
	{0, 1, 1, 1, 1, 1, 1, 1},
	{1, 1, 1, 1, 1, 1, 1, 1},
	{1, 1, 1, 1, 1, 1, 1, 1},
	{1, 1, 1, 1, 1, 1, 1, 1},
	{1, 1, 1, 1, 1, 1, 1, 1},
	{1, 1, 1, 1, 1, 1, 1, 1},
	{1, 1, 1, 1, 1, 1, 1, 1},
	{1, 1, 1, 1, 1, 1, 1, 1}
};
*/

#define PATHWAY_COLOUR 0
#define WALL_COLOUR 1
#define BLOCKED_COLOUR 2
#define PATH_COLOUR 3


int count = 0;

int findMazePAth(int x, int y) {
	if (x < 0 || y < 0 || x >= N || y >= N || maze[x][y] != PATHWAY_COLOUR)
		return 0;
	else if (x == N - 1 && y == N - 1) {
		return 1;
	}
	maze[x][y] = BLOCKED_COLOUR;
	count = findMazePAth(x - 1, y) + findMazePAth(x, y + 1) + findMazePAth(x + 1, y) + findMazePAth(x, y - 1);
	maze[x][y] = PATHWAY_COLOUR;
	return count;
}


/*
bool findMazePAth(int x, int y) {
	if (x < 0 || y < 0 || x >= N || y >= N || maze[x][y] != PATHWAY_COLOUR)
		return false;
	else if (x == N - 1 && y == N - 1) {
			maze[x][y] = PATH_COLOUR;
		return true;
	}
	maze[x][y] = PATH_COLOUR;
	if (findMazePAth(x - 1, y) || findMazePAth(x, y + 1) || findMazePAth(x + 1, y) || findMazePAth(x, y - 1)) {
		return true;
	}
	maze[x][y] = BLOCKED_COLOUR;
	return false;
}
*/

int main() {
/*	if (findMazePAth(0, 0) == true) {
		printf("True");
	}
	else printf("False");
	*/
	count = findMazePAth(0, 0);
	printf("%d", count);

}
