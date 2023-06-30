var notify_list = []
var temp_notify = null;

class Notify {
    constructor (id, time, mess) {
        this.id = id;
        this.time = time;
        this.mess = mess;
        this.render();
        this.attachEventListenner();
    }
    render() {
        const notify_div = $('<div>', {
            id: `${this.id}_notify`,
            class: 'notify_box_wrapper',
            html: `
            <div id="${this.id}_notify_box" class="notify_box">
                <div id="${this.id}_notify_time" class="notify_time">
                    <p id="${this.id}_notify_time_0">${this.time.split(" ")[0]}</p>
                    <p id="${this.id}_notify_time_1">${this.time.split(" ")[1]}</p>
                </div>
                <p id="${this.id}_notify_mess" class="notify_mess">${this.mess}</p>
                <a id="${this.id}_notify_del"class="notify_delete" href="#">x</a>
            </div>
            <hr>
            `
        });
        $("#notify_content_ctn").prepend(notify_div);
    }
    attachEventListenner() {
        $(`#${this.id}_notify_del`).on("click", ()=>{
            $("#notify_num").text(notify_list.length-1);
            MakeReq("/notify/delete", "DELETE", {id: this.id}).then((res)=>{
                if (res.code == 0) {
                    $(`#${this.id}_notify`).remove();
                    for (let i = 0; i < notify_list.length; i++) {
                        if (notify_list[i].id == this.id) {
                            notify_list.splice(i,1);
                            break;
                        }
                    }
                }
            })
        })
    }
}

function showNotify() {
    if ($("#notify_box_ctn").is(":visible")) {
        $("#notify_box_ctn").hide();
    } else {
        $("#notify_box_ctn").show();
    }
}

$("#notify_box_ctn").hide();

$(document).on("click", (event)=>{
    var target = event.target.outerHTML;
    var sample = target.substring(0, 20);
    console.log(sample);
    if(sample == `<html lang="en"><hea` || sample == `<div id="grid_node">` || sample == `<div id="grid_node"`) {
        $("#notify_box_ctn").hide();
    }
})

$("header").on("click",(event)=>{
    if ($("#nofity_btn").is(event.target)) {return;}
    $("#notify_box_ctn").hide();
})

MakeReq("/notify/getall", "GET", {}).then((res)=>{
    for (const notify of res) {
        temp_notify = new Notify(notify.id, notify.time, notify.mess);
        notify_list.push(temp_notify);
    }
    $("#notify_num").text(notify_list.length);
})


