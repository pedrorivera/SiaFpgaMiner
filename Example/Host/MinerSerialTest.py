#!/usr/bin/env python
import serial
import binascii

# Configure serial interface
ser = serial.Serial('/dev/ttyUSB0')  # open serial port
ser.baudrate = 115200

# Get some work from siad
# Block 975
merkleRoot = "6350916638e03107884f447e37ddd6093e8de171f49ef6be830f2495927756ef"
timestamp  = "56c6745500000000" #1433716310 reversed for LSB first tx
target     = "CCCCCCCC10000000"#"CCCCCCC000000000" # Reversed for LSB first tx
parent     = "0000000009e54a03f6738eafe76cf99e4382c8090ab08615b00b2e840fe24baf"
while 1:
	# Write out the work
	ser.write(binascii.a2b_hex(parent))
	ser.write(binascii.a2b_hex(target))
	ser.write(binascii.a2b_hex(timestamp))
	ser.write(binascii.a2b_hex(merkleRoot))

	print("Sent out the test work data, now run miner")

	# Wait for the response, read() is blocking
	nonce = ser.read(8)

	print("Nonce response: %s" %binascii.b2a_hex(nonce)) # check out response endianness
	#print("Expected: 0000f94300000000")

ser.close()