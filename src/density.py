import matplotlib.pyplot as plt
import numpy as np
import scienceplots
import scipy
import tqdm

from src.filter import Filter
from src.gigrn import gigrnd

plt.style.use("science")


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

    def chf_gig(self, u, a, b, p):
        return (
            (a / (a - 2j * u)) ** (p / 2)
            * scipy.special.kv(p, (b * (a - 2j * u)) ** 0.5)
            / scipy.special.kv(p, (b * a) ** 0.5)
        )

    def chf_bgig(self, u: complex, ndays: int):
        return (
            self.chf_gig(u, self.a1, self.b1, self.p1)
            * self.chf_gig(-u, self.a2, self.b2, self.p2)
        ) ** ndays

    def get_dens_fourier(self, x_array, ndays):
        dens = []
        print("Computing density (Fourier)...")
        for x in tqdm.tqdm(x_array):
            u = np.arange(-150, 150, 0.01)
            step_u = np.mean(np.diff(u))
            value_x = (np.exp(-1j * u * x) *
                       self.chf_bgig(u, ndays)).sum() * step_u
            dens.append(value_x)
        print("Computed!")
        return np.real(dens) / (2 * np.pi)

    #############################
    #### Calibrated Density #####
    #############################

    def save_calibratd_density(self):
        x = np.arange(-0.5, 0.5, self.step)
        dens_bgig_cal = self.dens_bgig(x)
        # Plotting the calibrated density
        # plt.style.use(["science", "ieee"])
        plt.figure(figsize=(8, 5))
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
        plt.close()

    ############################
    #### Simulate Process  #####
    ############################

    def simulate_one_bgig(self):
        bgigp = gigrnd(self.p1, self.a1, self.b1)
        bgigm = gigrnd(self.p2, self.a2, self.b2)
        return bgigp - bgigm

    def simulate_one_trajectory(self, ndays: int):
        value = 0
        for _ in range(ndays):
            value += self.simulate_one_bgig()
        return value

    def simulate_trajectories(self, ndays: int, Nsim: int):
        L = []
        print("Simulating...")
        for _ in tqdm.tqdm(range(Nsim)):
            L.append(self.simulate_one_trajectory(ndays))
        print("Simulated!")
        return L

    def plot_hist(self, ndays: int, Nsim: int):
        x = np.arange(-0.1, 0.1, 1e-3)
        dens_fourier = self.get_dens_fourier(x, ndays)
        values = self.simulate_trajectories(ndays, Nsim)
        plt.figure(figsize=(8, 5))
        plt.hist(values, density=True, bins=50,
                 label=rf"$t={ndays}$ (Simulated histogram)")
        plt.plot(x, np.real(dens_fourier), linestyle="-",
                 label="Fourier inversion")
        plt.title(rf"$t={ndays}$")
        plt.ylabel("Density")
        plt.xlabel(r"$x$")
        plt.legend()
        plt.grid()
        plt.savefig(f"output/process_simul_t_{ndays}")
