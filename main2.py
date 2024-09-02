from bgigestimator import BGIGEstimator
from esscherestimator import EsscherEstimator
from pricer import Density


def main():
    path = "HistoricalData_1719299483154.csv"
    bgig_est = BGIGEstimator(path)
    essch_est = EsscherEstimator(**bgig_est.params)
    pricer = Density(filter=bgig_est.filter, **bgig_est.params)
    pricer.save_calibratd_density()
    return


if __name__ == "__main__":
    main()
