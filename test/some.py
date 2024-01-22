import pyotp
import qrcode

# Assuming `username` is the identifier for each user
username = "user123"

# Generate a random secret key for each user

with open(f"{username}_key.key",'w') as file:
    file.write(pyotp.random_base32())

with open(f"{username}_key.key",'r') as key:
    contents = key.read()

# Create the TOTP URI and save the QR code
uri = pyotp.totp.TOTP(contents).provisioning_uri(
    name=username,
    issuer_name='GalacticCoder'
)
qrcode.make(uri).save(f'{username}_qr.png')

# Now, when verifying, use the generated secret_key
totp = pyotp.TOTP(contents)
verification = totp.verify(input("Enter the Code: "))
