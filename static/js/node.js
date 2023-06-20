let current_nodeID = ""
let current_name = ""

class Node {
    constructor(name, id, data) {
        this.name = name;
        this.id = id;
        this.data = data;
        this.state = false;
        this.render();
        this.attachEventListeners();
    }

    render() {
        const nodeDiv = $('<div>', {
            id: this.id,
            class: 'node',
            html: `
                <p class="node_name" id="${this.id}_node_name">${this.name}</p>
                    <form style="display: none" id="${this.id}_rename_form" onsubmit="handle_rename_node(event)">
                        <input id="new_name_input" type="text" name="new_name" placeholder="New name">
                    </form>
                <div class="setting_btn" id="${this.id}_setting">...</div>
                <br>
                <div id="${this.id}_node_data_ctn">
                    <p class="node_data" id="${this.id}_soil">Soil moisture: ${this.data.soil}%</p>
                    <p class="node_data" id="${this.id}_status">Status: ${this.data.status}</p>
                    <p class="node_data" id="${this.id}_time">Updated at: ${this.data.update_time}'</p>
                </div>
                <div class="setting_ele" id="${this.id}_node_setting_ctn">
                    <button id="${this.id}_detail">Detail</button>
                    <button id="${this.id}_rename">Rename</button>
                    <button id="${this.id}_delete">Delete</button>
                </div>
            `
        });

        nodeDiv.on('mouseleave', () => {
            if (this.state) {
                $(`#${this.id}_node_setting_ctn`).hide();
                $(`#${this.id}_node_data_ctn`).show();
                this.state = false;
            }
            $(`#${this.id}_node_name`).show();
            $(`#${this.id}_rename_form`).hide();
        });

        $('#grid_node').append(nodeDiv);
    }

    attachEventListeners() {
        $(`#${this.id}_setting`).on('click', () => {
            if (!this.state) {
                $(`#${this.id}_node_setting_ctn`).show();
                $(`#${this.id}_node_data_ctn`).hide();
                this.state = true;
            } else {
                $(`#${this.id}_node_setting_ctn`).hide();
                $(`#${this.id}_node_data_ctn`).show();
                this.state = false;
            }
        });

        $(`#${this.id}_rename`).on('click', () => {
            current_nodeID = this.id;
            current_name = this.name;
            $(`#${this.id}_node_name`).hide();
            $(`#${this.id}_rename_form`).show();
        });

        $(`#${this.id}_delete`).on('click', () => {
            let answer = confirm("Are you sure to delete this node?");
            if (!answer) {
                return;
            }
            PostReq('/delete_node', { id: this.id }).then((res) => {
                if (res.code === 0) {
                    $(`#${this.id}`).remove();
                    let count = 0;
                    for (let node of Node_list) {
                        if (node.id == `#${this.id}`) {
                            Node_list.splice(count,1);
                            break;
                        }
                        count++;
                    }
                }
            });
        });
    }
}

function handle_rename_node(event) {
    event.preventDefault();
    if ($("#new_name_input").val() == "" || $("#new_name_input").val() == current_name) return;
    PostReq(`/rename_node`, {id: current_nodeID, new_name: $("#new_name_input").val()}).then((res)=>{
        if (res.code != 0) { ErrorCodeHandle(res.code) }
        else {
            $(`#${current_nodeID}_rename_form`).hide();
            $(`#${current_nodeID}_node_name`).show();
            $(`#${current_nodeID}_node_name`).text($("#new_name_input").val());
        }
    })
}

class AddNode {
    constructor() {
        this.render();
    }
    render() {
        const addNode = $('<div>', {
            id: 'add_div',
            class: 'node',
            html: `
              <p class="node_name">Add new node</p><br>
              <div id="add_sign">
                <p class="node_data" style="font-size: 60px; font-weight: bold;">+</p>
              </div>
              <div id="add_form_ctn" style="display: none;">
                <form onsubmit="handle_add_node(event)">
                  <input id="input_name" name="name" style="width: 80%; height: 24px; margin-bottom: 8px;" type="text" placeholder="Node Name"><br>
                  <input id="input_id" name="id" style="width: 80%; height: 24px; margin-bottom: 8px;" type="text" placeholder="Node ID"><br>
                  <input style="width: 60%; height: 30px;" type="submit" value="Add">
                </form>
              </div>
            `
        });
        addNode.on('mouseover', () => {
            $('#add_sign').hide();
            $('#add_form_ctn').show();
        });
          
        addNode.on('mouseout', () => {
            $('#add_sign').show();
            $('#add_form_ctn').hide();
        });
        $("#grid_node").append(addNode);
    }
}

function handle_add_node(event) {
    event.preventDefault();
    if ($("#input_name").val() == "" || $("#input_id").val() == "") return;
    PostReq("/add_node", {name: $("#input_name").val(), id: $("#input_id").val()}).then((res)=>{
        if (res.code != 0) { ErrorCodeHandle(res.code) }
        else {
            temp_node = new Node($("#input_name").val(), $("#input_id").val(), {"soil": "0.00", "status": "Normal", "update_time": `${getFormatTime().split(" ")[0]} ${getFormatTime().split(" ")[1]}`});
            $('#add_div').remove();
            Node_list.push(temp_node);
            $('#grid_node').append(new AddNode);
        }
    })
}


  
