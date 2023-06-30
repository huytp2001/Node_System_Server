var socket = io.connect();

// Handle socket for stream sensor data
socket.on("stream", (data)=>{
    const data_array = data.split("|");
    $("#temp").text(data_array[1]);
    $("#hum").text(data_array[2]);
    if (parseInt(data_array[3]) < 500) {
        $("rain").text("Yes");
    } else {
        $("rain").text("No");
    }
    $("lux").text(data_array[4]);
})

// Handle socket for node data
socket.on("node", (data)=>{
    const data_array = data.split('!');
    let id = data_array[1]
    let value = data_array[2]
    for (let node of Node_list) {
        if (id == node.id) {
            node.update_data(value);
        }
    }
})

// Handle socket for push notification
socket.on("notify",(data)=>{
    const data_array = data.split("|");
    let id = data_array[0]
    let mess = data_array[1]
    let time = data_array[2]
    temp_notify = new Notify(id, time, mess);
    notify_list.push(temp_notify);
    $("#notify_num").text(notify_list.length);
})
