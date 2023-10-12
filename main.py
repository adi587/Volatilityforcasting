r,sigma=GARCH_simulate(N=750, sigma_i=0.2, alpha_r=0.2, beta_r=0.7, omega_r=0.1)
result=GARCH_train(r=r,sigma=sigma,alpha1=0.3,beta1=0.6,omega1=0.05)
print(result)
