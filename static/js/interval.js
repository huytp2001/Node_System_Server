var type_and_day = null;

$("#date_time").text(getFormatTime());

setInterval(()=>{
    $("#date_time").text(getFormatTime());
    if (getFormatTime().split(" ")[0] == "00:00") {
        location.reload();
    }
}, 60000);

setInterval(()=>{
    if (type_and_day != null) {
        handleChart(type_and_day.split(" ")[0], type_and_day.split(" ")[1]);
    }
}, 36000000);

