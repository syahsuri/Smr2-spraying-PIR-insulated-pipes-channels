#pip install opencv-python qrcode[pil]

import qrcode

# # Text you want to codify
# text = "Air duct shape 1"

# # Generate QR Code
# qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
# qr.add_data(text)
# qr.make(fit=True)

# # Create QR image
# image_qr = qr.make_image(fill_color="black", back_color="white")

# # Save the image in a file
# name_file = "qr_code1.png"
# image_qr.save(name_file)
# print(f"QR generated and saved as '{name_file}'")


# #-----------------------------------------------------------------------------------------------------

# # Text you want to codify
# text = "Air duct shape 2"

# # Generate QR Code
# qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
# qr.add_data(text)
# qr.make(fit=True)

# # Create QR image
# image_qr = qr.make_image(fill_color="black", back_color="white")

# # Save the image in a file
# name_file = "qr_code2.png"
# image_qr.save(name_file)
# print(f"QR generated and saved as '{name_file}'")


#-----------------------------------------------------------------------------------------------------
# Text you want to codify
text = "Duct_4_Jump"

# Generate QR Code
qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
qr.add_data(text)
qr.make(fit=True)

# Create QR image
image_qr = qr.make_image(fill_color="black", back_color="white")

# Save the image in a file
name_file = "Duct_4_Jump.png"
image_qr.save(name_file)
print(f"QR generated and saved as '{name_file}'")


#-----------------------------------------------------------------------------------------------------