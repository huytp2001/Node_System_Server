async function MakeReq(url, method, data) {
    try {
        const response = await fetch(url, {
            method: method,
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            throw new Error('Request failed');
        }
        return response.json();
    } catch (error) {
        throw new Error(error.message);
    }
}

function ErrorCodeHandle(code) {
    if (code == 1) {alert("Duplicate node ID error");}
    if (code == 2) {alert("Duplicate node name error");}
    if (code == 3) {alert("Over max length character (16 max) in node ID");}
    if (code == 4) {alert("Over max length character (16 max) in node name");}
}

function getFormatTime() {
    var currentDateTime = new Date();
    var hour = currentDateTime.getHours();
    var minute = currentDateTime.getMinutes();
    var day = currentDateTime.getDate();
    var month = currentDateTime.getMonth() + 1; 
    var year = currentDateTime.getFullYear()
    var formattedTime = `${('0'+hour).slice(-2)}:${('0'+minute).slice(-2)} ${day}/${month}/${year}`;
    return formattedTime;
}

function getFormatDate(reverse_day) {
    var currentDateTime = new Date();
    currentDateTime.setDate(currentDateTime.getDate() - reverse_day);
    var day = currentDateTime.getDate();
    var month = currentDateTime.getMonth() + 1; 
    var formattedTime = ('0' + day).slice(-2) + '-' + ('0' + month).slice(-2);
    return formattedTime;
}

function dashboard() {
    $("#chart_wrapper").hide();
    $("#grid_node").show();
}

function getAverage(array) {
    let sum = 0;
    for (let value of array) {sum += value;}
    return (sum/array.length).toFixed(2);
}

function getMax(array) {
    let max = array[0];
    let index = 0;
    for (let i = 0; i < array.length; i++) {
        if (array[i] > max) {
            max = array[i];
            index = i;
        }
    }
    return {value: max, index: index}
}

function getMin(array) {
    let min = array[0];
    let index = 0;
    for (let i = 0; i < array.length; i++) {
        if (array[i] < min) {
            min = array[i];
            index = i;
        }
    }
    return {value: min, index: index}
}

function getDuration(array, threshold) {
    let duration = 0;
    for (let i = 0; i < array.length; i++) {
        if (array[i] > threshold) {
            duration++;
        }
    }     
    return duration;
}