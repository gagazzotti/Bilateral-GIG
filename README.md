# Bilateral Generalized Inverse Gaussian distribution

[![Python badge](https://img.shields.io/badge/Python-3.11.11-0066cc?style=for-the-badge&logo=python&logoColor=yellow)](https://www.python.org/downloads/release/python-31111/)
[![Pylint badge](https://img.shields.io/badge/Linting-pylint-brightgreen?style=for-the-badge)](https://pylint.pycqa.org/en/latest/)
[![Ruff format badge](https://img.shields.io/badge/Formatter-Ruff-000000?style=for-the-badge)](https://docs.astral.sh/ruff/formatter/)

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

The simulation code for a one-sided GIG distribution was taken from the following [repository](https://github.com/getian107/PRScsx/tree/master). 

## Interesting ? 

If you have any questions, feel free to contact us. We will be more than happy to answer ! 😀

If you use it, a reference to the paper would be highly appreciated.

```
@misc{agazzotti2024bilateralgeneralizedinversegaussian,
      title={The bilateral generalized inverse Gaussian process with applications to financial modeling}, 
      author={Gaetano Agazzotti and Jean-Philippe Aguilar},
      year={2024},
      eprint={2407.10557},
      archivePrefix={arXiv},
      primaryClass={math.PR},
      url={https://arxiv.org/abs/2407.10557}, 
}
```

## Tested on

[![Ubuntu badge](https://img.shields.io/badge/Ubuntu-24.04-cc3300?style=for-the-badge&logo=ubuntu)](https://www.releases.ubuntu.com/24.04/)
[![Conda badge](https://img.shields.io/badge/conda-24.9.2-339933?style=for-the-badge&logo=anaconda)](https://docs.conda.io/projects/conda/en/24.9.x/)
[![Intel badge](https://img.shields.io/badge/CPU-%20i5_10210U%201.60GHZ-blue?style=for-the-badge&logo=intel)](https://www.intel.com/content/www/us/en/products/sku/195436/intel-core-i510210u-processor-6m-cache-up-to-4-20-ghz/specifications.html)

