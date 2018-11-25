## cs545-reinforcement-learning-project
---

Final Project for CS545 Machine Learning. 

Train an AI with reinforcement learning (specficially Q Learning with dynamic programming) to play the Snake game. 

*Team Members (listed alphabetically by first name)*: Chris McPherson, Michelle Duer

---

#### Q Learning Algorithm
Implementing a Markov Decision Process based Q-Learning Algorithm with a slight twist
on the matrix implementation for the Q-Table.

#### Snake Game
Source of original game is a tutorial for building snake with pygame:
  https://pythonspot.com/snake-with-pygame/

Many modifications were made to the original game:
  - code cleaned
    - changed snake/mouse positional initialization, data structure implementation and modifications to work better with Q learning algorithm
    - removed unnecessary if statements for checking movements
    - changed variable names
    - separated classes into different files
  - applied Q learning algorithm to turn the game into a reinforcement learning project
    - allows for human and AI play
  - collisions: added a wall collision function and simplified existing functions
  -	added count score, frames count, speed
  - used different visual components
