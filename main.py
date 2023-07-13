from flask import Flask, render_template, request, jsonify
import threading
import serial
from flask_socketio import SocketIO
import schedule
from routes import node as node_api
from routes import notify as notify_api
from query import data, node
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dangquochuy'
socketio = SocketIO(app)
app.config['TEMP'] = 0
app.config['HUM'] = 0
app.config['RAIN'] = 0
app.config['LUX'] = 0

send_flag = threading.Event()  
send_data = ""

def get_format_date(reverse_day):
    current_date = datetime.now()
    new_date = current_date - timedelta(days=reverse_day)
    day = new_date.day
    month = new_date.month
    formatted_date = "{:02d}-{:02d}".format(day, month)
    return formatted_date

def disease_diagnosis(data_array):
	if len(data_array) == 0:
		return []
	diseases = []
	avr_temp = 0
	avr_hum = 0
	avr_rain = 0
	for data in data_array:
		avr_temp += data[1]
		avr_hum += data[2]
		avr_rain += data[3]
	avr_temp = avr_temp / len(data_array)
	avr_hum = avr_hum / len(data_array)
	avr_rain = avr_rain / len(data_array)
	if avr_rain > 100 and avr_temp > 30 and avr_hum > 80:
		diseases.append("Bệnh đốm trắng")
	if avr_hum > 85 and avr_rain > 100:
		diseases.append("Bệnh đốm nâu")
	if avr_temp > 35:
		diseases.append("Bệnh nám cành") 
	if avr_rain > 100:
		diseases.append("Bệnh thối đầu cành")
	if avr_rain > 100 and avr_temp > 25 and avr_hum > 80:
		diseases.append("Bệnh thán thư") 
	return diseases

@app.route("/toggle_light")
def toggle_light():
	print("light")
	global send_data, send_flag
	send_flag.set()
	send_data = "toggle_light"
	return jsonify({"code": 0}), 200

@app.route("/toggle_water")
def toggle_water():
	print("water")
	global send_data, send_flag
	send_flag.set()
	send_data = "toggle_water"
	return jsonify({"code": 0}), 200

@app.route("/")
def index():
	data_obj = {
		'temp': app.config['TEMP'], 
		'hum': app.config['HUM'], 
		'rain': "Yes" if int(app.config['RAIN']) < 500 else "No", 
		'lux': app.config['LUX']
	}
	Data = data.DataChart()
	data_array = Data.fetch_data_limit(72)
	diseases = disease_diagnosis(data_array)
	return render_template("index.html", sensorData = data_obj, diseases=diseases)

@app.route("/chart", methods=["POST"])
def chart():
	Data = data.DataChart()
	body = request.get_json()
	data_array = Data.fetch_data_by_day_and_type(get_format_date(int(body["day"])), body["type"])
	return jsonify({"data": data_array}), 200

@app.route("/send_out", methods=["POST"])
def send_out():
	global send_flag, send_data
	body = request.get_json()
	send_flag.set()
	send_data = body["mess"]
	return jsonify({"code": 0}), 200

app.register_blueprint(node_api.bp)
app.register_blueprint(notify_api.bp)

def listen_serial():
	global send_flag, send_data
	port = 'COM5'  
	baudrate = 115200       
	ser = serial.Serial(port, baudrate)
	def tx_serial(mess):
		ser.write(mess.encode('utf-8'))
	def get_data_interval():
		mess = "give me data"
		ser.write(mess.encode('utf-8'))
	get_data_interval()
	schedule.every(1).hour.do(get_data_interval)
	while True:
		schedule.run_pending()
		line = ""
		if ser.in_waiting > 0:
			line = ser.readline().decode('utf-8').rstrip()
			print(line)
			data_array = line.split('|')
			if len(data_array) == 1:
				data_array = line.split('!')
				if data_array[0] == "node":
					socketio.emit("node", line)
					myNode = node.Node()
					myNode.update_node(data_array[1], data_array[2])
			if data_array[0] == "sensorstream":
				socketio.emit('stream', line)
				app.config['TEMP'] = data_array[1]
				app.config['HUM'] = data_array[2]
				app.config['RAIN'] = data_array[3]
				app.config['LUX'] = data_array[4]
			if data_array[0] == "sensordata":
				myData = data.DataChart()
				myData.insert_data(data_array[1], data_array[2], data_array[3], data_array[4])
		if send_flag.is_set():
			tx_serial(send_data)
			send_flag.clear()

if __name__ == "__main__":
	websocket_thread = threading.Thread(target=listen_serial)
	websocket_thread.daemon = True
	websocket_thread.start()
	socketio.run(app, host="0.0.0.0", port=5000, debug=True)


