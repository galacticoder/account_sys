import pyotp
import qrcode

# Replace 'secret_key' and 'username' with your actual values
secret_key = "siomeodsiklfjdshjfhjsdil8902893472918"
username = "GalacticCoder"

# Generate provisioning URI and save QR code
totp_auth = pyotp.totp.TOTP(secret_key).provisioning_uri(name=username, issuer_name='GalacticCoder')
qrcode.make(totp_auth).save("qr_auth.png")

# Create TOTP object for verification
totp_qr = pyotp.TOTP(secret_key)

# Prompt user for input
user_input = input("Enter the Code: ")

# Verify the entered code
verify = totp_qr.verify(user_input)

# Print the verification result
print(verify)
