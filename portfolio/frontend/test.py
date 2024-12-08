import re

contact_num = "09362702803"  # Example input

# Regular expression to validate exactly 11 digits, no other symbols allowed
if not re.match(r'^\d{11}$', contact_num):
    print("Contact number must be exactly 11 digits, with no symbols or spaces.")
else:
    print("Contact number is valid.")
