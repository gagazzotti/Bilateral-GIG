from bgigestimator import BGIGEstimator
from esscherestimator import EsscherEstimator
from density import Density


def main():
    path = "data/SP500_2021_2024.csv"
    bgig_est = BGIGEstimator(path)
    essch_est = EsscherEstimator(**bgig_est.params)
    pricer = Density(filter=bgig_est.filter, **bgig_est.params)
    pricer.save_calibratd_density()
    pricer.plot_hist(ndays=5, Nsim=10000)
    return


if __name__ == "__main__":
    main()
