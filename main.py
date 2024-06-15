from BIG.distribution import Distribution


def main():
    lambda_p = 2
    mu_p = 4
    lambda_m = 1
    mu_m = 5
    distribution = Distribution(lambda_p, mu_p, lambda_m, mu_m)
    # samples = distribution.draw_sample(6)
    # distribution.plot_distribution()
    # distribution.plot_histogram(10000)
    distribution.plot_distribution(xmin=-10, xmax=10)


if __name__ == "__main__":
    main()
