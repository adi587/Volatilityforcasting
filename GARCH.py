import math
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf


def GARCH_simulate(N,sigma_i,alpha_r,beta_r,omega_r):
    #N=500#2000     #no.data point
    sigma=[] #volatility
    sigma.append(sigma_i)
    r=list() #returns
    alpha_r=0.2
    beta_r=0.7
    omega_r=0.1

    for i in range(N):
        r.append(sigma[i]*np.random.normal())
        sigma=np.append(sigma,math.sqrt(omega_r+alpha_r*(r[i]**2)+beta_r*sigma[i]**2))

    #TO PLOT
    #plt.plot(range(N),r)
    #plt.plot(range(N+1),sigma)
    #plt.legend(['$u$','$\sigma$ estimate'])
    #plt.xlabel('Days')
    #plt.ylabel('Value')
    
    #plt.grid()
    #plt.show()
    return r,sigma
    
def GARCH_train(r,sigma,alpha1,beta1,omega1):
    opt = tf.keras.optimizers.Adam(learning_rate=0.004)
    N=len(r)
    alpha1=tf.Variable(alpha1)
    beta1=tf.Variable(beta1)
    omega1=tf.Variable(omega1)

    trainable_vars=[alpha1,beta1,omega1]
    @tf.function     
    def LF(alpha1,beta1,omega1):
        loss=float(0)   
        sigma_pred=float(r[0])
        for i in range(N):
            loss=loss+tf.math.log(2*math.pi*sigma_pred**2)+r[i]**2/sigma_pred**2
            sigma_pred=tf.math.sqrt(omega1+alpha1*(r[i]**2)+beta1*sigma_pred**2)
        return loss   

    for i in range(1000):
        with tf.GradientTape() as tp:
            ls=LF(alpha1,beta1,omega1)
        gradients = tp.gradient(ls, trainable_vars)
        opt.apply_gradients(zip(gradients, trainable_vars))
        

    sigma_rec=[float(r[0])]
    for i in range(N):
        sigma_rec=np.append(sigma_rec,math.sqrt(omega1.numpy()+alpha1.numpy()*(r[i]**2)+beta1.numpy()*sigma_rec[i]**2))
    return [alpha1.numpy(),beta1.numpy(),omega1.numpy()]
