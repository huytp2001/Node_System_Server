let clickFlag = false;
const timeout_milis = 5000;

function toggle_water() {
    if (clickFlag) return
    MakeReq("/toggle_water", "GET", {}).then((res)=>{
        if (res.code == 0) {
            if ($("#toggle_water").text() == "toggle_off") {
                $("#toggle_water").text("toggle_on");
            } else {
                $("#toggle_water").text("toggle_off");
            }
            clickFlag = true;
            setTimeout(()=>{
                clickFlag= false;
            },timeout_milis);
        }
    })
}

function toggle_light() {
    if (clickFlag) return
    MakeReq("/toggle_light", "GET", {}).then((res)=>{
        if (res.code == 0) {
            if ($("#toggle_light").text() == "toggle_off") {
                $("#toggle_light").text("toggle_on");
            } else {
                $("#toggle_light").text("toggle_off");
            }
            clickFlag = true;
            setTimeout(()=>{
                clickFlag= false;
            },timeout_milis);
        }
    })
}