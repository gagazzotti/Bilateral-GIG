import numpy as np


class BIG:
    def __init__(self, lambda_p: float, mu_p: float, lambda_m: float, mu_m: float):
        self.lambda_p = lambda_p
        self.mu_p = mu_p
        self.lambda_m = lambda_m
        self.mu_m = mu_m
        self._check_positivity()

    def set_params(self, params: list):
        if len(params) != 4:
            raise ValueError("Parameters should contain 4 elements.")
        else:
            self.lambda_p = params[1]
            self.mu_p = params[2]
            self.lambda_m = params[3]
            self.mu_m = params[4]
            self._check_positivity()

    def get_params(self) -> list:
        return [self.lambda_p, self.mu_p, self.lambda_m, self.mu_m]

    def _check_positivity(self):
        prod = np.prod(self.get_params())
        if prod < 0:
            raise ValueError("The parameters should be positive.")
