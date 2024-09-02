from bgig_distribution.bgigestimator import BGIGEstimator
from bgig_distribution.esscherestimator import EsscherEstimator
from bgig_distribution.density import Density


def main():
    path = "data/SP500_2021_2024.csv"
    bgig_est = BGIGEstimator(path)
    # essch_est = EsscherEstimator(**bgig_est.params)
    density = Density(filter=bgig_est.filter, **bgig_est.params)
    density.save_calibratd_density()
    density.plot_hist(ndays=5, Nsim=10000)
    return


if __name__ == "__main__":
    main()
