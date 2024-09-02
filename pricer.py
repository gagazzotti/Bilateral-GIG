import numpy as np
import matplotlib.pyplot as plt
import scipy

from filter import Filter


class Density:

    def __init__(
        self,
        a1: float,
        b1: float,
        p1: float,
        a2: float,
        b2: float,
        p2: float,
        filter: Filter,
        step=1e-4,
    ):
        self.a1 = a1
        self.b1 = b1
        self.p1 = p1
        self.a2 = a2
        self.b2 = b2
        self.p2 = p2
        self.step = step
        self.filter = filter
        return

    def dens_gig(self, x: float, a: float, b: float, p: float):
        value = (
            (a / b) ** (p / 2)
            * x ** (p - 1)
            * np.exp(-0.5 * (a * x + b / x))
            / (2 * scipy.special.kv(p, (a * b) ** 0.5))
            * (x > 0)
        )
        value[np.isnan(value)] = 0
        return value

    def dens_bgig(self, x: np.ndarray):
        # x = np.arange(-0.5, 0.5, self.step)
        dens_bgig_cal = (
            np.convolve(
                self.dens_gig(x, self.a1, self.b1, self.p1),
                self.dens_gig(x, self.a2, self.b2, self.p2)[::-1],
                mode="same",
            )
            * self.step
        )
        return dens_bgig_cal

    def save_calibratd_density(self):
        x = np.arange(-0.5, 0.5, self.step)
        dens_bgig_cal = self.dens_bgig(x)
        # Plotting the calibrated density
        plt.style.use(["science", "ieee"])
        plt.xlim(-0.1, 0.1)
        plt.plot(x, dens_bgig_cal, label="Calibrated \n BGIG")
        plt.hist(
            self.filter.log_returns_clean,
            density=True,
            bins=12,
            label="SP500",
            histtype="bar",
        )
        plt.xlabel(r"log-returns")
        plt.ylabel(r"Density")
        plt.grid()
        plt.legend(loc="upper right")
        plt.savefig("output/calibrated_density.png")
