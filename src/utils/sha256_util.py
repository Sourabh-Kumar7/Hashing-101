import math
from src.constants.sha2_constants import SHA256_CONSTANTS, SHA256_INITIAL_HASH_VALUES

class SHA256ConstantsGenerator:
    def __init__(self, prime_limit=1000):
        self.prime_limit = prime_limit

    def sieve_of_eratosthenes(self, n):
        """
        Implementation of the Sieve of Eratosthenes algorithm to generate prime numbers.

        Args:
            n (int): Generate prime numbers up to 'n'.

        Returns:
            List[int]: List of prime numbers up to 'n'.
        """
        sieve = [True] * (n + 1)
        sieve[0] = sieve[1] = False
        prime_numbers = []

        for current in range(2, n + 1):
            if sieve[current]:
                prime_numbers.append(current)
                for multiple in range(current * current, n + 1, current):
                    sieve[multiple] = False

        return prime_numbers

    def generate_initial_hash_values(self, required_primes_cnt=8):
        """
        Generate the initial hash values using the square roots of prime numbers.

        Args:
            required_primes_cnt (int): Number of prime numbers to use.

        Returns:
            List[int]: List of initial hash values.
        """
        required_primes = self.sieve_of_eratosthenes(self.prime_limit)[:required_primes_cnt]
        initial_hash_values = []

        for prime in required_primes:
            # Calculate the square root
            sqrt = math.sqrt(prime)
            # Extract the fractional part
            fractional_part = sqrt - int(sqrt)
            # Convert the fractional part to a 32-bit hexadecimal value
            hex_value = format(int(fractional_part * (2**32)), '08x')
            # Append the result to the initial hash values
            hash_value = int(hex_value, 16)
            initial_hash_values.append(hash_value)

        return initial_hash_values

    def generate_sha256_round_constants(self, required_primes_cnt=64):
        """
        Generate SHA-256 round constants using the cube roots of prime numbers.

        Args:
            required_primes_cnt (int): Number of prime numbers to use.

        Returns:
            List[int]: List of SHA-256 round constants.
        """
        required_primes = self.sieve_of_eratosthenes(self.prime_limit)[:required_primes_cnt]
        round_constants = []

        for prime in required_primes:
            # Calculate the cube root
            cube_root = prime ** (1/3)
            # Extract the fractional part
            fractional_part = cube_root - int(cube_root)
            # Convert the fractional part to a 32-bit hexadecimal value
            hex_value = format(int(fractional_part * (2**32)), '08x')
            # Append the result to the round constants
            hex_value_str = int(hex_value, 16)
            round_constants.append(hex_value_str)

        return round_constants

# if __name__ == "__main__":
#     generator = SHA256ConstantsGenerator(prime_limit=1000)
#
#     # Get the initial hash values
#     hash_values = generator.generate_initial_hash_values()
#     print(hash_values)
#     print(SHA256_INITIAL_HASH_VALUES)
#
#     if hash_values == SHA256_INITIAL_HASH_VALUES:
#         print("Matched SHA256_INITIAL_HASH_VALUES")
#
#     # Get the SHA-256 round constants
#     k = generator.generate_sha256_round_constants()
#     print(k)
#     print(SHA256_CONSTANTS)
#
#     if k == SHA256_CONSTANTS:
#         print("Matched SHA256_CONSTANTS")
