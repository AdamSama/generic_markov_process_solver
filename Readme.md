# A generic Markov process solver
## It solves both a Markov Decision Process and a Markov Reward Process
The input file consists of 4 types of input lines:
</br>
Rewards/costs lines of the form 'name = value' where value is an integer
Edges of the form 'name : [e1, e2, e2]' where each e# is the name of an out edge from name
Probabilities of the form 'name % p1 p2 p3'</br>
    A = 7</br>
    B % .9</br>
    C : [ B, A]</br>
    C=-1</br>
    A : [B, A]</br>
    A % .2 .8</br>
    B : [A, C]</br>
</br>
The algorithm I use is value iteration + policy iteration as shown below:
```javascript
    𝜋 = initial policy (arbitrary)
    V = initial values (perhaps using rewards)
    for {
      V = ValueIteration(𝜋) // computes V using stationery P
      𝜋' = GreedyPolicyComputation(V) // computes new P using latest V
      if 𝜋 == 𝜋' then return 𝜋, V
      𝜋 = 𝜋'
    }
```
The program takes 4 flags:
* -df : a float discount factor [0, 1] to use on future rewards, defaults to 1.0 if not set
* -min : minimize values as costs, defaults to false which maximizes values as rewards
* -tol : a float tolerance for exiting value iteration, defaults to 0.001
* -iter : an integer that indicates a cutoff for value iteration, defaults to 50
To run the program, simply type "python solver.py + input text name" and you can add flags like "min, tol, iter, df" </br>
sample input:
```bash
python solver.py -df .9 -tol 0.0001 input.txt
```