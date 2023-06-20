const chartPreset = {
    temp: {
        label: "Temperature (*C)",
        color: "rgba(235, 106, 47, 0.5)",
        maxValue: 80,
        prefix: "*C"
    },
    hum: {
        label: "Humidity (%)",
        color: "rgba(14, 75, 156, 0.5)",
        maxValue: 100,
        prefix: "%"
    },
    rain: {
        label: "Rain percent (%)",
        color: "rgba(9, 214, 204, 0.5)",
        maxValue: 100,
        prefix: "%"
    },
    lux: {
        label: "Light level (lx)",
        color: "rgba(226, 230, 18, 0.5)",
        maxValue: 1000,
        prefix: "lx"
    }
}

var myChart = null;

function handleChart(type, day) {
    PostReq(`/chart`, { type: type, day: day }).then((res) => {
        console.log(res.data);
        $("#grid_node").hide();
        $("#chart_wrapper").show();
        $("#title").text(`${chartPreset[type]["label"]} on ${getFormatDate(day)}`);
        let chart_data = []
        for (let value of res.data) {if (value == -1) {chart_data.push(0);} else {chart_data.push(value);}}
        console.log(chart_data);
        const data = {
            labels: ["0h", "1h", "2h", "3h", "4h", "5h", "6h", "7h", "8h", "9h", "10h", "11h", "12h", "13h", "14h", "15h", "16h", "17h", "18h", "19h", "20h", "21h", "22h", "23h"],
            datasets: [{
                label: chartPreset[type]["label"],
                data: chart_data,
                backgroundColor: chartPreset[type]["color"],
                borderColor: chartPreset[type]["color"],
                borderWidth: 2
            }]
        };
        const ctx = document.getElementById('myChart').getContext('2d');
        ctx.canvas.width = (window.innerWidth/100)*70;
        if (myChart != null) {
            myChart.destroy();
        }
        myChart = new Chart(ctx, {
            type: 'bar',
            data: data,
            options: {
                responsive: false,
                maintainAspectRatio: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        suggestedMax: chartPreset[type]["maxValue"]
                    }
                }
            }
        });
        for (let i = 0; i < 7; i++) {
            $(`#day-${i}`).text(getFormatDate(i));
            $(`#day-${i}`).attr("onclick", `handleChart("${type}", ${i})`);
        }
        $("#average").text(`${getAverage(chart_data)}${chartPreset[type]["prefix"]}`);
        $("#max").text(`${getMax(chart_data).value}${chartPreset[type]["prefix"]} (${getMax(chart_data).index}h)`);
        $("#min").text(`${getMin(chart_data).value}${chartPreset[type]["prefix"]} (${getMin(chart_data).index}h)`);
        if (type == "rain" || type == "lux") {
            $("#duration").show();
            if (type == "rain") { $("#duration_value").text(`${getDuration(chart_data, 400)}h`); }
            if (type == "lux") { $("#duration_value").text(`${getDuration(chart_data, 100)}h`); }
        } else {
            $("#duration").hide();
        }
    })
}

