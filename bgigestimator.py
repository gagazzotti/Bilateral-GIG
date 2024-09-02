import numpy as np
import scipy.special
import tqdm

from filter import Filter


class BGIGEstimator:

    def __init__(self, path: str):
        self.filter = Filter(path)
        self.estimate_a()
        self.get_empirical_moments()
        self.calibrate_bp_pm()
        self.display_error()
        return

    #######################################
    ######### Estimation of a_+/- #########
    #######################################

    def estimate_a(self):
        x = np.arange(1, len(self.filter.cummax) + 1)
        self.a1 = 2 * ((self.filter.cummax / np.log(x))[-1]) ** (-1)
        self.a2 = -2 * ((self.filter.cummin / np.log(x))[-1]) ** (-1)
        print(self.a1, self.a2)
        return

    ##############################################
    ######## Moments of BGIG distribution ########
    ##############################################

    def moments_estimator(self, sequence: np.ndarray, order: int) -> float:
        N = len(sequence)
        match order:
            case 1:
                return np.sum(sequence) / N
            case 2:
                return np.sum((sequence - self.moments_estimator(sequence, 1)) ** 2) / N
            case 3:
                return np.sum((sequence - self.moments_estimator(sequence, 1)) ** 3) / (
                    N * self.moments_estimator(sequence, 2) ** (3 / 2)
                )
            case 4:
                return np.sum((sequence - self.moments_estimator(sequence, 1)) ** 4) / (
                    N * self.moments_estimator(sequence, 2) ** 2
                )

    def R(self, omega: float, p: float) -> float:
        return scipy.special.kv(p + 1, omega) / scipy.special.kv(p, omega)

    def c1(self, omega: float, eta: float, p: float):
        return self.R(omega, p) * eta

    def c2(self, omega: float, eta: float, p: float):
        polynom = -self.R(omega, p) ** 2 + (2 * (p + 1) / omega) * self.R(omega, p) + 1
        return polynom * eta**2

    def c3(self, omega: float, eta: float, p: float):
        polynom = (
            2 * self.R(omega, p) ** 3
            - (6 * (p + 1) / omega) * self.R(omega, p) ** 2
            + ((4 * (p + 1) * (p + 2) / omega**2) - 2) * self.R(omega, p)
            + 2 * (p + 1) / omega
        )
        return polynom * eta**3

    def c4(self, omega: float, eta: float, p: float):
        polynom = (
            2 * self.R(omega, p) ** 3
            - (6 * (p + 1) / omega) * self.R(omega, p) ** 2
            + ((4 * (p + 1) * (p + 2) / omega**2) - 2) * self.R(omega, p)
            + 2 * (p + 1) / omega
        )
        return polynom * eta**4

    def get_cumulants(
        self,
        omega1: float,
        omega2: float,
        eta1: float,
        eta2: float,
        p1: float,
        p2: float,
        order: int,
    ):
        match order:
            case 1:
                return self.c1(omega1, eta1, p1) - self.c1(omega2, eta2, p2)
            case 2:
                return self.c2(omega1, eta1, p1) + self.c2(omega2, eta2, p2)
            case 3:
                return self.c3(omega1, eta1, p1) - self.c3(omega2, eta2, p2)
            case 4:
                return self.c4(omega1, eta1, p1) + self.c4(omega2, eta2, p2)
            case _:
                raise NotImplementedError

    def moment_from_cumul(
        self,
        omega1: float,
        omega2: float,
        eta1: float,
        eta2: float,
        p1: float,
        p2: float,
        order: int,
        step: float,
    ):
        match order:
            case 1:
                return step * self.get_cumulants(omega1, omega2, eta1, eta2, p1, p2, 1)
            case 2:
                return step * self.get_cumulants(omega1, omega2, eta1, eta2, p1, p2, 2)
            case 3:
                return self.get_cumulants(omega1, omega2, eta1, eta2, p1, p2, 3) / (
                    self.get_cumulants(omega1, omega2, eta1, eta2, p1, p2, 2) ** (3 / 2)
                    * step**0.5
                )
            case 4:
                return (
                    self.get_cumulants(omega1, omega2, eta1, eta2, p1, p2, 4)
                    / (
                        self.get_cumulants(omega1, omega2, eta1, eta2, p1, p2, 2) ** 2
                        * step**0.5
                    )
                    + 3
                )

    ##########################################
    ######## Estimation of b_+/-,p+/- ########
    ##########################################

    def get_empirical_moments(self):
        self.m1 = self.moments_estimator(self.filter.log_returns_clean, 1)
        self.m2 = self.moments_estimator(self.filter.log_returns_clean, 2)
        self.m3 = self.moments_estimator(self.filter.log_returns_clean, 3)
        self.m4 = self.moments_estimator(self.filter.log_returns_clean, 4)
        self.step = 1

    def objective_function(self, vars: list):
        b1, p1, b2, p2 = vars
        omega1 = (self.a1 * b1) ** 0.5
        omega2 = (self.a2 * b2) ** 0.5
        eta1 = (self.a1 / b1) ** (-0.5)
        eta2 = (self.a2 / b2) ** (-0.5)
        # print(omega1, omega2, eta1, eta2)
        equal1 = self.m1 - self.moment_from_cumul(
            omega1, omega2, eta1, eta2, p1, p2, order=1, step=self.step
        )
        equal2 = self.m2 - self.moment_from_cumul(
            omega1, omega2, eta1, eta2, p1, p2, order=2, step=self.step
        )
        equal3 = self.m3 - self.moment_from_cumul(
            omega1, omega2, eta1, eta2, p1, p2, order=3, step=self.step
        )
        equal4 = self.m4 - self.moment_from_cumul(
            omega1, omega2, eta1, eta2, p1, p2, order=4, step=self.step
        )
        return np.power(
            [equal1 / self.m1, equal2 / self.m2, equal3 / self.m3, equal4 / self.m4], 2
        ).sum()

    def calibrate_bp_pm(self):
        bounds = [(0.01, 10), (-20, 20), (0.01, 10), (-20, 20)]
        options = {
            # "disp": True,  # Display convergence messages
            "ftol": 1e-15,  # Tolerance for termination
            "maxiter": 1000,
        }
        errors = []
        params = []
        print("Calibrating...")
        for i in tqdm.tqdm(range(10)):
            point = (
                np.random.rand() * 50,
                (np.random.rand() - 0.5) * 50,
                np.random.rand() * 50,
                (np.random.rand() - 0.5) * 50,
            )

            solution = scipy.optimize.minimize(
                self.objective_function, point, bounds=bounds, options=options, tol=1e-5
            )
            errors.append(self.objective_function(solution.x))
            params.append(solution.x)
        print("Calibrated!")
        best_param_idx = np.argmin(errors)
        self.b1, self.p1, self.b2, self.p2 = params[best_param_idx]
        self.params = {
            "a1": self.a1,
            "b1": self.b1,
            "p1": self.p1,
            "a2": self.a2,
            "b2": self.b2,
            "p2": self.p2,
            # "filter": self.filter,
        }

    def display_error(self):
        omega1 = (self.a1 * self.b1) ** 0.5
        omega2 = (self.a2 * self.b2) ** 0.5
        eta1 = (self.a1 / self.b1) ** (-0.5)
        eta2 = (self.a2 / self.b2) ** (-0.5)

        self.m1_emp = self.moment_from_cumul(
            omega1, omega2, eta1, eta2, self.p1, self.p2, 1, 1
        )
        self.m2_emp = self.moment_from_cumul(
            omega1, omega2, eta1, eta2, self.p1, self.p2, 2, 1
        )
        self.m3_emp = self.moment_from_cumul(
            omega1, omega2, eta1, eta2, self.p1, self.p2, 3, 1
        )
        self.m4_emp = self.moment_from_cumul(
            omega1, omega2, eta1, eta2, self.p1, self.p2, 4, 1
        )
        empirical = {1: self.m1, 2: self.m2, 3: self.m3, 4: self.m4}
        estimate = {1: self.m1_emp, 2: self.m2_emp, 3: self.m3_emp, 4: self.m4_emp}

        for order in empirical.keys():
            print(
                f"Order n°{order}, Absolute Error: {np.format_float_scientific(np.abs(empirical[order] - estimate[order]), 5)}",
                f"Relative: {np.format_float_scientific(np.abs(np.abs(empirical[order] - estimate[order]) / empirical[order]) , 5)}",
                f"Empirical moment: {np.format_float_scientific(empirical[order],5)}",
                f"Estimated moment: {np.format_float_scientific(estimate[order],5)}",
            )
