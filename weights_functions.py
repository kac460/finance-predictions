# Returns reverse of [0.5, 0.25, 0.125, ..., 2^(-1*num_weights)]
def exponential_weights(num_weights):
    return [2**(-1*i) for i in reversed(range(1, num_weights+1))]


def even_weights(num_weights):
    return [1]*num_weights

# Returns [1, 2, ..., num_weights]
def incrementing_weights(num_weights):
    return list(range(1, num_weights+1))
