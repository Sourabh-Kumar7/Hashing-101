import struct
from src.utils.sha256_util import SHA256ConstantsGenerator


class SHA256:
    """
    SHA-256 hashing algorithm implementation.
    """

    def __init__(self):
        """
        Initialize the SHA-256 hash object with initial hash values and constants.
        """
        generator = SHA256ConstantsGenerator()
        self.h0, self.h1, self.h2, self.h3, self.h4, self.h5, self.h6, self.h7 = generator.generate_initial_hash_values()
        self.k = generator.generate_sha256_round_constants()

    def _right_rotate(self, x, n):
        """
        Perform a right rotation (circular shift) of 'x' by 'n' bits.

        Args:
            x: Input integer.
            n: Number of bits to rotate.

        Returns:
            Rotated integer.
        """
        return ((x >> n) | (x << (32 - n))) & 0xFFFFFFFF

    def _preprocess_message(self, message):
        """
        Preprocess the input message by padding and converting it to bytes.

        Args:
            message: Input string message.

        Returns:
            Padded and converted message as bytes.
        """
        message_bytes = message.encode('utf-8')
        bit_length = len(message_bytes) * 8
        message_bytes += b'\x80'
        while (len(message_bytes) + 8) % 64 != 0:
            message_bytes += b'\x00'
        message_bytes += struct.pack('>Q', bit_length)
        return message_bytes

    def hash_string(self, message):
        """
        Compute the SHA-256 hash of the input string.

        Args:
            message: Input string to be hashed.

        Returns:
            SHA-256 digest as bytes.
        """
        message_bytes = self._preprocess_message(message)
        words = [0] * 64
        for i in range(0, len(message_bytes), 64):
            chunk = message_bytes[i:i + 64]
            for j in range(16):
                words[j] = struct.unpack('>I', chunk[j * 4:j * 4 + 4])[0]

            for j in range(16, 64):
                s0 = self._right_rotate(words[j - 15], 7) ^ self._right_rotate(words[j - 15], 18) ^ (words[j - 15] >> 3)
                s1 = self._right_rotate(words[j - 2], 17) ^ self._right_rotate(words[j - 2], 19) ^ (words[j - 2] >> 10)
                words[j] = (words[j - 16] + s0 + words[j - 7] + s1) & 0xFFFFFFFF

            a, b, c, d, e, f, g, h = self.h0, self.h1, self.h2, self.h3, self.h4, self.h5, self.h6, self.h7

            for j in range(64):
                S1 = self._right_rotate(e, 6) ^ self._right_rotate(e, 11) ^ self._right_rotate(e, 25)
                ch = (e & f) ^ ((~e) & g)
                temp1 = h + S1 + ch + self.k[j] + words[j]
                S0 = self._right_rotate(a, 2) ^ self._right_rotate(a, 13) ^ self._right_rotate(a, 22)
                maj = (a & b) ^ (a & c) ^ (b & c)
                temp2 = S0 + maj

                h = g
                g = f
                f = e
                e = (d + temp1) & 0xFFFFFFFF
                d = c
                c = b
                b = a
                a = (temp1 + temp2) & 0xFFFFFFFF

            self.h0 = (self.h0 + a) & 0xFFFFFFFF
            self.h1 = (self.h1 + b) & 0xFFFFFFFF
            self.h2 = (self.h2 + c) & 0xFFFFFFFF
            self.h3 = (self.h3 + d) & 0xFFFFFFFF
            self.h4 = (self.h4 + e) & 0xFFFFFFFF
            self.h5 = (self.h5 + f) & 0xFFFFFFFF
            self.h6 = (self.h6 + g) & 0xFFFFFFFF
            self.h7 = (self.h7 + h) & 0xFFFFFFFF

        digest = struct.pack('>I', self.h0) + struct.pack('>I', self.h1) + struct.pack('>I', self.h2) + struct.pack('>I', self.h3) + \
            struct.pack('>I', self.h4) + struct.pack('>I', self.h5) + struct.pack('>I', self.h6) + struct.pack('>I', self.h7)

        return digest

if __name__ == "__main__":
    sha256_hasher = SHA256()
    message = ""
    result = sha256_hasher.hash_string(message)
    print(f"Original String: {message}")
    print(f"SHA-256 Hash: {result.hex()}")

# e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
# e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855