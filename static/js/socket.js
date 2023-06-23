var socket = io.connect();

// Handle socket
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
// Handle socket
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