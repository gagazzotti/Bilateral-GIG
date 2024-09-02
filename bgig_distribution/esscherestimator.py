import numpy as np
import scipy
import tqdm


class EsscherEstimator:

    def __init__(
        self, a1: float, b1: float, p1: float, a2: float, b2: float, p2: float
    ):
        self.a1 = a1
        self.b1 = b1
        self.p1 = p1
        self.a2 = a2
        self.b2 = b2
        self.p2 = p2
        self.calibrate_theta()

    def psiGIG(self, u: complex, a: float, b: float, p: float):
        return np.log(
            (a / (a - 2j * u)) ** (p / 2)
            * scipy.special.kv(p, (b * (a - 2j * u)) ** 0.5)
            / scipy.special.kv(p, (b * a) ** 0.5)
        )

    def psiBGIG(
        self,
        u: complex,
    ):
        return self.psiGIG(u, self.a1, self.b1, self.p1) + self.psiGIG(
            -u, self.a2, self.b2, self.p2
        )

    def objective(self, theta: float):
        first = self.psiBGIG(-1j * (theta + 1))
        second = self.psiBGIG(-1j * (theta))
        res = np.real(first - second)
        return np.abs(res) ** 2

    def calibrate_theta(self):
        options = {
            # "disp": True,  # Display convergence messages
            "ftol": 1e-15,  # Tolerance for termination
            "maxiter": 1000,
        }
        errors = []
        params = []
        print("Calibrating...")
        for x0 in tqdm.tqdm(np.arange(-100, 100, 20)):
            solution = scipy.optimize.minimize(
                self.objective,
                [x0],
                bounds=[(-500, 500)],
                tol=1e-15,
                options=options,
                method="L-BFGS-B",
            )
            errors.append(self.objective(solution.x))
            params.append(solution.x)
        print("Calibrated!")
        best_param_idx = np.argmin(errors)
        self.theta = params[best_param_idx]
        print("Theta", self.theta, "Error", np.min(errors))
