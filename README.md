# Assignment 2 Report

### Part 1: IJK
1. What is the game about:
This is a two player fully observable game which is similar to 2048 game and has four possible moves - (Up, Down, Left, Right). Pairs of letters that are same, and adjacent to each other, in the direction of the movement are combined together to create a single tile of subsequent letter. 
- Ex- A + a -> B(if the move is made by + player)
- Ex - A + a -> b (if the move is made by - player)

This has two variants, deterministic and non-deterministic.
- Deterministic - When a move is made, a new 'A' or 'a' tile is generated at a predictable empty position on the board. The code keeps checking for an empty position starting from the first tile and checks till the last.
- Non Deterministic - When a move is made, a new 'A' or 'a' tile is generated at a random empty position on the board.
- The major task of this assignment is to write a smart enough AI which can beat a human or any other AI.

Initial State - 6X6 board with one 'A'
State space - All boards with any of A to K letters (lower case or upper cae)
Successor Function - Gives the board which is effected by one of the four moves (L, R, U, D)
Goal State - Two cases - a board with one 'K' or 'k', other case is fully filled board (player with the higher letter case will win)

2. Solving the deterministic case:
- For the AI to predict the best move, we need to elaborate and create a tree with all possible outcomes. We expect that everyone makes the best move. This is nothing but the min-max algorithm. This algorithm helps us in calculating the best possible outcome at a given state.
- Obviously the whole tree cannot be built to find out the best possible move. That would need insane amount of time. That is when limiting the search to a certain depth would help. Here by using proper evaluation functions(The possiblity of a state to win)we find the chance of winning for the MAX node which is propagated up the tree.
- The problem with this approach is we go through the whole tree which might seem unnecessary. This is when alpha-beta pruning comes to rescue. By calculating the alpha value of a parent, we can prune out any children which might not be useful. By calculating these values properly, we are able to prune out any children which would not change the alpha or beta values of the parent.
- For now, we are limitting the depth of the tree to 7. Once the tree reaches a depth limit of 8, the evaluation function comes into picture and the recurssion stops. The value calculated is sent back to the parent node where the alpha beta values and the scores are kept track of. The minimum value of these scores are sent back to the min node and the maximum score of the children are sent back to the max node.
- Based on the best scores of the children of the root node(The initial node), a move is decided and sent back to the IJK.py

3. Solving Non Deterministic case:
- This is very similar to the deterministic case.
- The only difference is, once the make move function is invoked, the place where the 'A' or the 'a' tile is placed is completely arbitary.
- This is why we wrote our own logic using the logic of logic_IJK.py. The chance node can just make a move('L R U D') but cannot add a tile. 
- The next node, min or max respectively adds these tiles in all the possible functions. Similar to min-max tree, these values are propagated up the tree. The min node propagates the min value, the max node propagates the max value and the chance node sends the averaged out value from the below nodes.

Heuristic
We have explored several heuristics by going through the ideas implemented for 2048 game. To convert this IJK case to 2048 case and to get a numeric for evaluated best winning board, we converted letters to 2^alphabetical order. These explored heuristics are dot product of board with heavily weighted corners, monotonicity, smoothness and empty tiles. All these heuristics give equal evaluation irrespective of ‘+’ player or ‘-‘ player. So we considered only differentiating functions that give different evaluations for both the players. In doing so, we have implemented:

- Same case adjacent letters have heavy weights: In this we again have higher heavy weights for later coming letters compared to that of early coming letters
- Number of later coming letters have high weights compared to early coming letters in the board
- Above two values are calculated for both max and min player. We finally take evaluation value as the max player eval – min player eval


### Part 2: Horizon finding
1.	Simplest Bayes net approach: Using simple bayes net where each state(Si) is independent of one another and each observation(Wi) is just dependent on corresponding State(Si)
- Our observable values are from the intensities of edge strength image which is P(Si|Wi)
- To find the horizon of the given image, we just use the argmax of edge strength to find the ridge vector
![equation]( https://latex.codecogs.com/gif.latex?%5Cinline%20s_%7Bi%7D%5E%7B*%7D%20%3D%20arg%20%5Cmax_%7Bs_%7Bi%7D%7D%20P%28S_%7Bi%7D%3Ds_%7Bi%7D%7Cw_%7B1%2C...%2C%7Dw_%7Bm%7D%29%20%5C%5C%20s_%7Bi%7D%5E%7B*%7D%20%3D%20arg%20%5Cmax_%7Bs_%7Bi%7D%7D%20P%28S_%7Bi%7D%3Ds_%7Bi%7D%29*P%28S_%7Bi%7D%3Ds_%7Bi%7D%7Cw_%7Bi%7D%29)
- All rows are equally likely in each of the column, so P(Si) will be 1/n and therefore edge strength is enough to find the horizon in this case
- We directly take arg max of edge strength in each column and use this as ridge in our actual image
- This is a very simple case and it doesn’t give the best results because gradient could be highest for non-horizon cases also
2.	Viterbi algorithm to solve for the maximum a posterior estimate
- Similarly, Our observable values are from the intensities of edge strength image
- To find the horizon of image, we find the max edge strength row for each column by the method of Viterbi
- Here each column is time sequence, and each row is the state 
- Viterbi variables along with sequence with max probability to reach that state are stored in a matrix
- In this viterbi case:
  - Start probability for each row is 1/n where n is max number of rows 
  - Emission Probability:
  
  ![equation](https://latex.codecogs.com/gif.latex?%5Cinline%20e_%7Bi%7D%28O_%7Bj%7D%29%20%3D%20x_%7Bi%2Cj%7D/%5Csum_%20j%20x_%7Bi%2Cj%7D)
  - Transition Probability: 
  
  ![equation](https://latex.codecogs.com/gif.latex?%5Cinline%20P_%7Bij%7D%20%3D%20l*%5Cexp%5E%7B-l*%7Cx%7C%7D%20%5C%20where%20%5C%20x%20%3D%20i-j)
  
  After trying out different values for parameter(l), we finally chose l = 3.5
  
  
- Major challenges faced are with the images that have a continuous higher gradient shift for non-horizon segments of the image
3.	Human feedback case - We follow the same steps as Viterbi, except that we take emission probability at (x,y) as 1 to force the horizon pass through this point (x,y) 
