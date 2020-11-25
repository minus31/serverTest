import math
import numpy as np 

def smoothing_factor(t_e, cutoff):
    r = 2 * math.pi * cutoff *  t_e# keep t_e = 1 always
    return r / (r + 1)

def exponential_smoothing(a, x, x_prev):
    return a * x + (1 - a) * x_prev

def filter(x_0, x_1, min_cutoff=10, beta=0.001, d_cutoff=1.0):
    t_e = 1
    a_d = smoothing_factor(t_e, d_cutoff)
    dx = (x_1 - x_0)
    dx_hat = exponential_smoothing(a_d, dx, dx)

    cutoff = min_cutoff + beta * abs(dx_hat)
    a = smoothing_factor(t_e, cutoff)
    x_hat = exponential_smoothing(a, x_1, x_0)

    return x_hat

class OneEuroFilter:
    def __init__(self, 
                x0,
                dx0=0.0, 
                min_cutoff=1.0, 
                beta=0.0,
                d_cutoff=1.0):
        """Initialize the one euro filter."""
        # The parameters.
        self.min_cutoff = min_cutoff
        self.beta = beta
        self.d_cutoff = d_cutoff
        # Previous values.
        self.x_prev  = x0
        # self.dx_prev = dx0
        # self.t_prev  = t0

    def __call__(self, x):
        """Compute the filtered signal."""
        t_e = 1

        # The filtered derivative of the signal.
        a_d = smoothing_factor(t_e, self.d_cutoff)
        dx = (x - self.x_prev) / t_e
        dx_hat = exponential_smoothing(a_d, dx, dx)

        # The filtered signal.
        cutoff = self.min_cutoff + self.beta * abs(dx_hat)
        a = smoothing_factor(t_e, cutoff)
        x_hat = exponential_smoothing(a, x, self.x_prev)

        # Memorize the previous values.
        self.x_prev = x_hat
        # self.dx_prev = dx_hat
        # self.t_prev = t

        return x_hat