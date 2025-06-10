from src.bgigestimator import BGIGEstimator
from src.density import Density
from src.esscherestimator import EsscherEstimator


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
