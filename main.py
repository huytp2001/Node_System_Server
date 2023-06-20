from flask import Flask, render_template, request, redirect, url_for, jsonify
import threading
import serial
from flask_socketio import SocketIO
from query import *
import schedule
from utils import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dangquochuy'
socketio = SocketIO(app)
app.config['TEMP'] = 0
app.config['HUM'] = 0
app.config['RAIN'] = 0
app.config['LUX'] = 0

send_flag = threading.Event()  
send_data = ""

gb_data = DataChart()
gb_node = Node()

@app.route("/send_out", methods=["POST"])
def send_out():
	global send_flag, send_data
	body = request.get_json()
	send_flag.set()
	send_data = body["mess"]
	return jsonify({"code": 0}), 200

@app.route("/")
def index():
	node_array = gb_node.fetch_all_node()
	data_obj = {
		'temp': app.config['TEMP'], 
		'hum': app.config['HUM'], 
		'rain': "Yes" if int(app.config['RAIN']) < 500 else "No", 
		'lux': app.config['LUX']
	}
	return render_template("index.html", sensorData = data_obj, node_array=node_array)

@app.route("/chart", methods=["POST"])
def chart():
	body = request.get_json()
	# sensor_obj = {
	# 	'temp': app.config['TEMP'], 
	# 	'hum': app.config['HUM'], 
	# 	'rain': "Yes" if int(app.config['RAIN']) < 500 else "No", 
	# 	'lux': app.config['LUX']
	# }
	data_array = gb_data.fetch_data_by_day_and_type(get_format_date(int(body["day"])), body["type"])
	# myChart = None
	# if chart == "temp":
	# 	myChart = Chart("Temperature (*C)", "rgba(235, 106, 47, 0.5)", 80, 0, "*C")
	# if chart == "hum":
	# 	myChart = Chart("Humidity (%)", "rgba(14, 75, 156, 0.5)", 100, 0, "%")
	# if chart == "rain":
	# 	myChart = Chart("Rain percent (%)", "rgba(9, 214, 204, 0.5)", 100, sum(1 for element in data_array if element > 10), "%")
	# if chart == "lux":
	# 	myChart = Chart("Light level (lx)", "rgba(226, 230, 18, 0.5)", 1000, sum(1 for element in data_array if element > 20), "lx")
	# chart_obj = {
	# 	"label": myChart.label,
	# 	"col_color": myChart.col_color,
	# 	"max_value": myChart.max_value,
	# 	"data": data_array
	# }
	# data = [num for num in data_array if num != -1]
	# try:
	# 	sta_obj = {
	# 		"average": f"{round(sum(data)/len(data),2)}{myChart.prefix}",
	# 		"max": {
	# 			"value": f"{max(data)}{myChart.prefix}",
	# 			"index": data_array.index(max(data_array))
	# 		},
	# 		"min": {
	# 			"value": f"{min(data)}{myChart.prefix}",
	# 			"index": data_array.index(min(data_array))
	# 		},
	# 		"duration": myChart.duration
	# 	}
	# except:
	# 	sta_obj = {
	# 		"average": 0,
	# 		"max": {
	# 			"value": 0,
	# 			"index": 0
	# 		},
	# 		"min": {
	# 			"value": 0,
	# 			"index": 0
	# 		},
	# 		"duration": 0
	# 	}
	return jsonify({"data": data_array}), 200

@app.route("/add_node", methods=["POST"])
def add_node():
	body = request.get_json()
	name = body["name"]
	id = body["id"]
	query_code = gb_node.insert_node(id, name, 1024)
	return jsonify({"code": str(query_code)}), 200

@app.route("/rename_node", methods=["POST"])
def rename_node():
	print("Hello")
	body = request.get_json()
	query_code = gb_node.rename_node(body["id"], body["new_name"])
	print(query_code)
	return jsonify({"code": str(query_code)}), 200

@app.route("/delete_node", methods=["POST"])
def delete_node():
	data = request.get_json()
	id = data["id"]
	gb_node.delete_node(id)
	return jsonify({"code": 0}), 200

@app.route("/notify", methods=["GET"])
def get_notify():
	return redirect(url_for("index"))

@app.route("/delete_table")
def delete_table():
	gb_data.delete_table()
	return redirect(url_for('index'))

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
					myNode = Node()
					myNode.update_node(data_array[1], data_array[2])
			if data_array[0] == "sensorstream":
				socketio.emit('stream', line)
				app.config['TEMP'] = data_array[1]
				app.config['HUM'] = data_array[2]
				app.config['RAIN'] = data_array[3]
				app.config['LUX'] = data_array[4]
			if data_array[0] == "sensordata":
				myData = DataChart()
				myData.insert_data(data_array[1], data_array[2], data_array[3], data_array[4])
		if send_flag.is_set():
			tx_serial(send_data)
			send_flag.clear()

if __name__ == "__main__":
	websocket_thread = threading.Thread(target=listen_serial)
	websocket_thread.daemon = True
	websocket_thread.start()
	socketio.run(app, host="0.0.0.0", port=5000, debug=True)


