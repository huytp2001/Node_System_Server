from datetime import datetime, timedelta
import serial

class Chart():
	def __init__(self, label, col_color, max_value, duration, prefix):
		self.label = label
		self.col_color = col_color
		self.max_value = max_value
		self.duration = duration
		self.prefix = prefix

def get_format_date(reverse_day):
    current_date = datetime.now()
    new_date = current_date - timedelta(days=reverse_day)
    day = new_date.day
    month = new_date.month
    formatted_date = "{:02d}-{:02d}".format(day, month)
    return formatted_date

def sendOverSerial(data):
	port = '/dev/ttyUSB0'  
	baudrate = 9600       
	ser = serial.Serial(port, baudrate)
	ser.write(data.encode('utf-8'))
	