#!/usr/bin/env python
import serial, binascii, time, requests

# Make sure siad is running with miner module and wallet has been unlocked through siac

# Configure serial interface
ser = serial.Serial('/dev/ttyUSB0')  # open serial port
ser.baudrate = 115200
ser.timeout = 0 # make it non-blocking

# Siad API request data
url = 'http://localhost:9980/miner/header'
headers = {'User-Agent': 'Sia-Agent'}

lastParent = ''

while 1:
	# Get some work from siad
	response = requests.get(url, headers=headers)
	if response.status_code != 200:
		print("Error: unexpected API response")

	# Format the block data as the FPGA expects it
	target = response.content[7::-1] # Includes reversal
	parent = response.content[32:64]
	tmstmp = response.content[72:80]
	merkle = response.content[80:112]
	workHeader = parent + target + tmstmp + merkle

	# Send new work if the block is new
	if parent != lastParent:
		print("New work!")
		ser.write(workHeader)
		lastParent = parent

	# Read the serial interface
	nonce = ser.read(8)
	if nonce != '':
		print("Found solution! nonce = %s" %binascii.b2a_hex(nonce))
		# Submit response. UART sends LSB first so Nonce is already LSB...MSB 
		minedHeader = parent + nonce + tmstmp + merkle
		post = requests.post(url, data=minedHeader, headers=headers)
		print(post.text)

	time.sleep(1) # Delay to avoid getting work data too often



ser.close()

