from BIG.BIG import BIG
import scipy.stats as stats
import numpy as np
import matplotlib.pyplot as plt

plt.style.use(["science", "ieee"])


class Distribution(BIG):
    def __init__(self, lambda_p: float, mu_p: float, lambda_m: float, mu_m: float):
        super().__init__(lambda_p, mu_p, lambda_m, mu_m)

    def draw_sample(self, n_samples: int):
        if n_samples <= 0:
            raise ValueError("Number of samples should be positive")

        pos = self._draw_positive(n_samples)
        neg = self._draw_negative(n_samples)
        return pos + neg

    def _draw_positive(self, n_samples: int):
        return stats.invgauss.rvs(
            mu=self.mu_p / self.lambda_p, loc=0, scale=self.lambda_p, size=n_samples
        )

    def _draw_negative(self, n_samples: int):
        return -stats.invgauss.rvs(
            mu=self.mu_m / self.lambda_m, loc=0, scale=self.lambda_m, size=n_samples
        )

    def distribution_positive(self, x: np.ndarray):
        dist_pos = np.zeros(len(x))
        dist_pos[x > 0] = (self.lambda_p / (2 * np.pi * x[x > 0] ** 3)) ** 0.5 * np.exp(
            -self.lambda_p * (x[x > 0] - self.mu_p) ** 2 / (2 * self.mu_p**2 * x[x > 0])
        )
        return dist_pos

    def distribution_negative(self, x: np.ndarray):
        dist_neg = np.zeros(len(x))
        dist_neg[x < 0] = (
            self.lambda_m / (2 * np.pi * (np.abs(x[x < 0])) ** 3)
        ) ** 0.5 * np.exp(
            -self.lambda_m
            * (-x[x < 0] - self.mu_m) ** 2
            / (2 * self.mu_m**2 * np.abs(x[x < 0]))
        )

        return dist_neg

    def distribution(self, x: np.ndarray):
        step = np.mean(np.diff(x))
        dist_pos = self.distribution_positive(x)
        dist_neg = self.distribution_negative(x)
        return step * np.convolve(dist_pos, dist_neg, mode="same")

    # plot to put in another class (Visualizer ? ) ?
    def plot_distribution(
        self,
        plot_dens_semi: bool = True,
        xmin: float = -50,
        xmax: float = 50,
        step: float = 0.01,
        color: str = "black",
    ):
        x = np.arange(xmin, xmax, step)
        plt.figure(figsize=(10, 4))
        plt.title(f"BIG{tuple(self.get_params())}")
        plt.plot(x, self.distribution(x), label=r"$f_\mathrm{BIG}$", color=color)

        if plot_dens_semi:
            plt.plot(
                x,
                self.distribution_negative(x),
                label=r"$f_-$",
                color="red",
                linestyle="-",
                alpha=0.5,
            )
            plt.plot(
                x,
                self.distribution_positive(x),
                label=r"$f_+$",
                color="green",
                linestyle="-",
                alpha=0.5,
            )

        plt.xlim(xmin, xmax)
        plt.legend()
        plt.grid()
        plt.xlabel(r"$x$", fontsize=10)
        plt.ylabel("Density", fontsize=10)
        plt.show()

    def plot_histogram(
        self,
        n_samples: int,
        plot_dens: bool = True,
        plot_dens_semi: bool = True,
        bins: int = 500,
        alpha: float = 0.6,
        color: str = "g",
        xmin: float = -15,
        xmax: int = 15,
        add_precision: float = 50,
    ):
        sample = self.draw_sample(n_samples)
        x = np.arange(xmin - add_precision, xmax + add_precision, step=0.01)

        plt.figure(figsize=(6, 15))
        plt.title(rf"Histogram of BIG, $n={n_samples}$")

        if plot_dens:
            plt.plot(x, self.distribution(x), label=r"$f_\mathrm{BIG}$", color=color)
        if plot_dens_semi:
            plt.plot(x, self.distribution_negative(x), label=r"$f_+$", color="orange")
            plt.plot(x, self.distribution_positive(x), label=r"$f_-$", color="blue")

        plt.hist(sample, density=True, bins=bins, alpha=alpha, color=color)
        plt.xlim(xmin, xmax)
        plt.legend()
        plt.grid()
        plt.xlabel(r"$x$")
        plt.ylabel("Density")
        plt.show()
