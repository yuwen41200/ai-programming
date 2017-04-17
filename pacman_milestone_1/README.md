## Usage ##

* P1-1

  `python pacman.py -p CleanerAgent -l P1-1`

* P1-2

  `python pacman.py -p FroggerAgent -l P1-2 -g StraightRandomGhost`

* P1-3

  `python pacman.py -p SnakeAgent -l P1-3 -g StraightRandomGhost`

* P1-4

  `python pacman.py -p DodgeAgent -l P1-4`

* P2-1

  `python pacman.py -l mediumMaze -p SearchAgent -a fn=dfs`  
  `python pacman.py -l tinyMaze -p SearchAgent -a fn=dfs`  
  `python pacman.py -l smallMaze -p SearchAgent -a fn=dfs`  
  `python pacman.py -l bigMaze -z 0.5 -p SearchAgent -a fn=dfs`  
  `python autograder.py -q q1`

* P2-2

  `python pacman.py -l mediumMaze -p SearchAgent -a fn=bfs`  
  `python pacman.py -l tinyMaze -p SearchAgent -a fn=bfs`  
  `python pacman.py -l smallMaze -p SearchAgent -a fn=bfs`  
  `python pacman.py -l bigMaze -z 0.5 -p SearchAgent -a fn=bfs`  
  `python autograder.py -q q2`

* P2-3

  `python pacman.py -l mediumMaze -p SearchAgent -a fn=astar,heuristic=manhattanHeuristic`  
  `python pacman.py -l tinyMaze -p SearchAgent -a fn=astar,heuristic=manhattanHeuristic`  
  `python pacman.py -l smallMaze -p SearchAgent -a fn=astar,heuristic=manhattanHeuristic`  
  `python pacman.py -l bigMaze -z 0.5 -p SearchAgent -a fn=astar,heuristic=manhattanHeuristic`  
  `python autograder.py -q q4`
