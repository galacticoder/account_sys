import pyotp

# Create a secret key (keep it secret!)̥
secret_key = pyotp.random_base32()

# Generate an OTP using HOTP
hotp = pyotp.HOTP(secret_key)

print("Your HMAC-based OTP at counter 0:", hotp.at(0))
print("Your HMAC-based OTP at counter 1:", hotp.at(1))
print("Your HMAC-based OTP at counter 2:", hotp.at(2))
