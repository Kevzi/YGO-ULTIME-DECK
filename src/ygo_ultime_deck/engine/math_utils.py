import math

def log_binom(n: int, k: int) -> float:
    """
    Calculate the natural logarithm of the binomial coefficient "n choose k".
    Uses the relationship: ln(n!) = math.lgamma(n + 1)
    ln(C(n, k)) = ln(n!) - ln(k!) - ln((n-k)!)
    """
    if k < 0 or k > n:
        return -float('inf')  # log(0)
    
    return math.lgamma(n + 1) - math.lgamma(k + 1) - math.lgamma(n - k + 1)

def calculate_hypergeometric(population_size: int, success_in_population: int, sample_size: int, successes_in_sample: int) -> float:
    """
    Calculate the hypergeometric probability using logarithmic math to avoid overflow.
    
    Parameters:
        population_size (int): N, the total number of items.
        success_in_population (int): K, the total number of success items in population.
        sample_size (int): n, the number of items drawn.
        successes_in_sample (int): k, the number of successes drawn.
        
    Returns:
        float: The exact probability of drawing exactly `k` successes.
    """
    N = population_size
    K = success_in_population
    n = sample_size
    k = successes_in_sample

    # Impossible scenarios
    if k < 0 or k > n or k > K or (n - k) > (N - K):
        return 0.0
    
    if N <= 0 or n <= 0:
        return 0.0

    # P(X=k) = C(K, k) * C(N-K, n-k) / C(N, n)
    # log(P) = log(C(K, k)) + log(C(N-K, n-k)) - log(C(N, n))
    
    log_p = log_binom(K, k) + log_binom(N - K, n - k) - log_binom(N, n)
    
    try:
        probability = math.exp(log_p)
        # Cap at 1.0 due to potential floating point inaccuracies
        return min(max(probability, 0.0), 1.0)
    except OverflowError:
        # If log_p is very large negative, math.exp can raise underflow/overflow or return 0
        # For standard hypergeometric this won't be positive overflow since P <= 1 => log_p <= 0
        return 0.0
