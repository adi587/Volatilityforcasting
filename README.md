# GARCH

# GARCH model 
Firstly we see how volatility is defined. $u_i=\frac{S_i-S_{i-1}}{S_{i-1}}$ were $S_i$ is stock price at day $i$ and $u_i$ is the percentage change in price between day $i$ and $i-1$. We assume $\tilde{u}=\frac{1}{m}$ $\sum_{i=1,m} u_{n-i}=0$ were $\tilde{u}$ is average percentage change of stock price on day $n$ out of $m$ observations of $u_i$. The reason why this can be assumed to be 0 is explained in J.Hull: Options, Futures and Other Derivatives. The volatility on day $n$ is given as $\sigma_n^2=\frac{1}{m}$ $\sum_{i=1,m} u^2_i$. The GARCH(1,1) model to predict volatility for day $n$ is $\sigma_n^2=\gamma V_L+\alpha u_{n-1}^2+\beta \sigma_{n-1}^2$ ($V_L$ is the long running average variance rate and $\gamma+\alpha+\beta=1$). This is a type of exponentially weighted moving average model (recent observations of $u_i$ matter more to the current volatility estimate than later ones). $\sigma_{n-1}^2$ here is the estimated volatility the previous day (through the model). This model only requires knowledge of the previous day's data (the data for days before this is all encoded in the predicted $\sigma_{n-1}^2$. The GARCH model has several useful properties. Firstly it predicts (correctly) volatility to be mean reverting to $V_L$. This can be done by showing through the GARCH model, variance predictions (V) satisfies $dV=\gamma (V_L-V)dt+(\alpha/\sqrt{2})Vdz$ ($z$ is Weiner process). The 'strength' of this 'pull' back to $V_L$ is determined by $\gamma$. To understand the other 2 terms we can look at the GARCH model recursively. When substituting the $\sigma_{n-1}^2$ and $\sigma_{n-2}^2$ predictions to $\sigma_n^2$ we see: $\sigma_n^2=\gamma V_L+\gamma\beta V_L+\gamma \beta^2 V_L+\alpha u_{n-1}^2+\alpha \beta u_{n-2}^2+\alpha \beta^2u_{n-3}^2+\beta^3\sigma_{n-3}^2$. This shows that $\beta$ can be interpreted as a decay rate between the importance of subsequent observations in predicting volatility. I.E if $\beta$ is large then $u_{n-2},u_{n-3}$ play more importance to what the total volatility should be than if $\beta$ were small. To use this model we need to find the most likely parameters of $\gamma,\alpha,\beta$ given a dataset of price movements. Setting $\omega=\gamma V_L$ gives $\sigma_n^2=\omega+\alpha u_{n-1}^2+\beta \sigma_{n-1}^2$ which is the model we will implement (we will find optimal $\omega,\alpha,\beta$).

# Simulating data
To find the optimal parameters we first assume the underlying price distribution is lognormal. So an observation of $u_i$ should occur with likelihood $\sim \frac{1}{\sqrt{2\pi\sigma_i^2}}\exp{\frac{-u_i^2}{2\sigma_i^2}}$ where $\sigma_i^2$ is the variance for day $i$. Given set of $n$ observations the likelihood that the set of $u_i$'s are observed is $\Pi_{i=1}^m \frac{1}{\sqrt{2\pi\sigma_i^2}}\exp{\frac{-u_i^2}{2\sigma_i^2}}$. The best estimate of $\sigma_i$ is the one that maximizes this likelihood function. However attempting to do this on a function that multiplies the different observations is hard, instead the logarithm can be taken which (ignoring constant terms) gives $\sum_{i=1,m} -\ln (\sigma_i^2)-\frac{u_i^2}{\sigma_i^2} $. As the log function is monotonically increasing, minimising $\sum_{i=1,m} \ln {\sigma_i^2}+\frac{u_i^2}{\sigma_i^2}$ is equivalent to maximising the likelihood function. To do this in practice an Adam optimiser is used. 

To first test how long it takes the model to converge simulation data was first generated. This is done by predetermining ($\alpha,\beta,\omega$) which were set to $0.2,0.7,0.1$ initially. Then an initial $\sigma_0$ is provided from which the first $u$ movement is sampled using a normal distribution ($u=\sigma N(0,1)$, where $N(0,1)$ is standard normal distribution). The next $\sigma$ is then estimated through the GARCH model to sample the next $u$. This process is repeated giving multiple $u$ which simulate a price movement that follows the GARCH model. The optimizer is then used on this data to find the original parameters. A simulated price movement is shown here:

![image](https://github.com/adi587/Volatilityforcasting/assets/63116085/42e07492-6b79-4c63-bf99-10a7e6623c84)


The volatility can be seen to be mean reverting. Furthermore, in areas of large price movements, the volatility increases to simulate a high volatility period before reverting back.

# Applying optimizer
I first simulated data for 500,750,1000 days 5 times each. The initial 'guess' of the parameters were $0.3,0.6,0.05$ for $\alpha,\beta,\omega$ respectively. I set the learning rate of the ADAM optimizer to 0.004 (played around with a few different rates but this seemed to work best, when I do a more formal investigation, I will post the results here). Here are the predicted parameters using the optimizer.

![image](https://github.com/adi587/Volatilityforcasting/assets/63116085/d321a33a-c542-4b89-abc5-2c46dd8e388d) ![image](https://github.com/adi587/Volatilityforcasting/assets/63116085/62e62903-cc6a-42a4-a9f6-69631fd4c32f) ![image](https://github.com/adi587/Volatilityforcasting/assets/63116085/526162a8-b1ae-4dbc-82b2-9a85fd095b79)
![image](https://github.com/adi587/Volatilityforcasting/assets/63116085/dcfba064-e612-48d2-88c4-0e96a135fe50) ![image](https://github.com/adi587/Volatilityforcasting/assets/63116085/d2b7b024-321d-48cf-a308-1da26d48f750) ![image](https://github.com/adi587/Volatilityforcasting/assets/63116085/5228be83-9596-4e99-8012-f78b24ff98a1)







(Note the $\omega$ range increasing from 500 days to 750 days is confusing. I suppose this is an anomaly since this doesn't follow the trend of the other parameters.)




I plotted the mean and range of values for each day (used range instead of standard deviation to illustrate the wide span of values possible from even a small set of perfectly GARCH simulated set of data). As can be seen, there is a large range in the parameter estimates. However, the means do tend towards the actual values as the days sampled are increased. The range can also be seen to decrease the more days that are sampled. I tried to run the optimizer on days longer than 1000, 
but my computer took too long to find a predicted value, hence I was limited in the sample space I could investigate. Note that this price movement was completely simulated to perfectly follow a GARCH volatility process. Therefore, using this model on real-world data should give us worse results. Given the already large range of predicted parameters in this idealized situation, I do not think this optimizer and model will do well on real-world data with the current maximum day range I can use. This is because even if the data follows the GARCH model closely we'd still be away from the true value due to the large range, reducing its effectiveness in predicting volatility. We would have to use a larger sample space to give accurate GARCH parameters from which volatility can be forecasted. 

Another interesting observation is that the range in parameter estimates for 1000 days seems to always be $\sim 0.045$ compared to the other days that vary substantially depending on the parameter. I am not sure why it becomes so stable, I assume the 'randomness' in parameter estimations is reduced (imagine a probability distribution for each parameter becoming more spiked to the true value) and so the predictions are usually fixed within a bound regardless of parameter. Any higher deviations become rapidly unlikely. A 'shallower' spike for lower $N$ means for 5 samples the 'distributions tails' are not sampled much giving a wider range of maximums and minimums for different parameters. In other words, if we assume a normal distribution centered at the true parameter values and only use 3 data sets, were $X_i$ is the parameter estimate for i'th data set, $max(X_1,X_2,X_3)-min(X_1,X_2,X_3)$ has a lower variance (as well as being smaller) the larger $N$ is. This gives less variation in the range between parameters for higher $N$.


A possible way the optimizing process could be sped up is by first remembering that the long-running volatility average is $V_L=\frac{\omega}{1-\alpha-\beta}$. We could estimate this by averaging volatility in our given sample space. Then we set $\omega=V_L(1-\alpha-\beta)$. This means we only need to optimize the program for two parameters now ($\alpha$ and $\beta$). This should cut down the program running time by a lot allowing me to sample over much larger day ranges. Note however there runs a risk that the $V_L$ we calculate over this day range is not the 'true' $V_L$ (the selected days may just have really high or low volatility which isn't representative of the actual long-term average volatility), but sampled over a large number of days this error should be minimal. I will try to incorporate this into the code later on and see if it improves performance. 

(Note: in main.py I only included code to run the program. I do not include any of the plotting code as I thought it was unnecessary)

