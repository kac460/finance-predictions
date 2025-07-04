# Returns reverse of [0.5, 0.25, 0.125, ..., 2^(-1*num_weights)]
def exponential_weights(num_weights: int) -> list[float]:
    return [2 ** (-1 * i) for i in reversed(range(1, num_weights + 1))]


def even_weights(num_weights: int) -> list[float]:
    return [1] * num_weights


_MONTHS_IN_YEAR = 12


def even_weights_last_year_only(num_weights: int) -> list[float]:
    if num_weights <= _MONTHS_IN_YEAR:
        return even_weights(num_weights)
    ignore = [0] * (num_weights - _MONTHS_IN_YEAR)
    use = [1] * _MONTHS_IN_YEAR
    return ignore + use


# Returns [1, 2, ..., num_weights]
def incrementing_weights(num_weights: int) -> list[float]:
    return list(range(1, num_weights + 1))


def weighted_avg(vals, weights):
    assert len(vals) == len(weights)
    return sum([vals[i] * weights[i] for i in range(len(vals))]) / sum(weights)
