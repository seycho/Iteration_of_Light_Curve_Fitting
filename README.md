# Iteration of Light Curve Fitting   
Iterate least-squares and gradient-descent to search best parameters process for fitting light curve as Fourier series. Fourier series form is determined by 1993 SM Rucinski.   
$I(\theta) = \sum{a_n cos(2 \pi n \theta)}$   
Adjust period $P$ and initial time $t_0$ in cosin function.   
$I(\theta) = \sum{a_n \frac{cos(2 \pi n (\theta - t_0))}{P}}$   
For easily calculate best parameters, Seperate finding process as two. 
One is least-squares process for measuring coefficient parameters of fourier series as $a_n$. 
And other is gradienr descent process for measuring period and initial time parameters.   
   
## Least-Squares Fitting
Actually it can be measured just using gradient descent that Fourier series parameters for $a_n$, $P$, $t_0$. 
However when process calculate all of these parameters, it takes a lot of time and computer resources. 
Even as a number of parameters are increased, required resources are much more increases exponentially.   
Then we get best parameters $a_n$ series values for using least-squares method with assumed $P$ and $t_0$ are constant values. 
For measuring minimum of $\chi^2$ which indicator calculating results of measuring best parameters, it needs to find $a_n$ parameters when derivative of $\chi^2$ became zero.
That shows.   
$$ \frac{\partial}{\partial a} \sum{(I(\theta)-M(\theta)})^2=0 $$   
It can show as matrix.   

$$\eqalign{
F\times A = M,\\
F = \left[
\begin{array}{cc}
    \sum 1&\sum C(b)&\sum C(2b)&\sum C(3b) \\
    \sum C(b)&\sum C(b)^2&\sum C(b)C(2b)&\sum C(b)C(3b) \\
\sum C(2b)&\sum C(b)C(2b)&\sum C(2b)^2&\sum C(2b)C(3b) \\
\sum C(3b)&\sum C(b)C(3b)&\sum C(2b)C(3b)&\sum C(3b)^2 \\
\end{array}
\right],\\
A = \left[
\begin{array}{cc}
    a_0\\
    a_1\\
    a_2\\
    a_3\\
\end{array}
\right],\;
M = \left[
\begin{array}{cc}
    \sum M(\theta) \\
    \sum M(\theta)C(b) \\
    \sum M(\theta)C(2b) \\
    \sum M(\theta)C(3b) \\
\end{array}
\right]
}$$   


## Gradient Descent Fitting   
