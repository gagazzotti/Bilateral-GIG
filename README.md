# Bilateral Generalized Inverse Gaussian distribution

The code allows to calibrate the BGIG distribution introduced in [*The bilateral generalized inverse Gaussian process with applications to financial modeling*](https://arxiv.org/abs/2407.10557) by Gaetano AGAZZOTTI and Jean-Philippe AGUILAR. The calibration is achieved with a moment-based method.

Calibration is done on SP500 index from 2021 to 2023.

## How to use ? 
First, provide the data path:
```
path = "data/SP500_2021_2024.csv"
```
Define the parameters estimator and the density builder with:
```
bgig_est = BGIGEstimator(path)
# essch_est = EsscherEstimator(**bgig_est.params)
density = Density(filter=bgig_est.filter, **bgig_est.params)
```
You can finally either get the calibrated density or the process simulation for $t\in\mathbb{N}$ in the output folder using:
```
density.save_calibratd_density()
density.plot_hist(ndays=5, Nsim=10000)
```
Enjoy!

## Credits

The simulation code for a one-sided GIG distribution was took from the following [repository](https://github.com/getian107/PRScsx/tree/master). 