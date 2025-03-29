import os
import sys
import re
import qianfan
import asyncio
import json
import websockets
import yaml

from flask import Flask, render_template, request, jsonify

# 获取当前文件的绝对路径
current_dir = os.path.dirname(os.path.abspath(__file__))
# 增加子目录到系统路径
ha_ws_dir = os.path.join(current_dir, 'ha_ws')
sys.path.append(ha_ws_dir)    
ha_file_dir = os.path.join(current_dir, 'ha_file')
sys.path.append(ha_file_dir)    
import ha_ws
import ha_auto_cfg

# 从文件读取并解密
with open('/usr/web_server/ha_copilot.dat', 'r') as f:
    lines = f.readlines()
    os.environ["QIANFAN_ACCESS_KEY"] = ha_auto_cfg.read_key(lines[0], "ha_copilot").decode()
    os.environ["QIANFAN_SECRET_KEY"] = ha_auto_cfg.read_key(lines[1], "ha_copilot").decode()

chat_comp = qianfan.ChatCompletion()
def create_ha_ws():
    # 指定要创建的目录路径
    # src_path = '/usr/custom_components/ha_copilot'
    # dst_path = '/homeassistant/custom_components/ha_copilot'
    # 创建目录
    # copy_directory(src_path, dst_path)

    # base_path = '/homeassistant'
    # traverse_directory(base_path)
    
    # ha_auto_cfg.print_cfg_auto_yaml()
    ha_auto_cfg.get_auto_script_list()

    app = Flask(__name__)  

    asyncio.run(ha_ws.ha_ws_get_device_list())
    asyncio.run(ha_ws.ha_ws_get_label_list())
    asyncio.run(ha_ws.ha_ws_get_area_list())
    
    return app  

# 在应用入口点（如 WSGI 服务器配置或运行脚本）中调用工厂函数  
app = create_ha_ws()

def get_chat_response(model_text):
    # 指定特定模型
    resp = chat_comp.do(model="ERNIE-Speed-128k", messages=[{
        "role": "user",
        "content": model_text,
    }])
    # print('chat completion done')
    
    #print(resp["body"]["result"])
    # body_str = '```stesd```sdd'
    yaml_match = re.search(r'```([^```\\]|\\.)*```', resp["body"]["result"])
    if(yaml_match == None):
        yaml_str = resp["body"]["result"]
    else:
        yaml_str   = '# ' + re.sub(r'```', "", yaml_match.group(0))
    return yaml_str

@app.route('/', methods=['GET', 'POST'])
def home():
    #print(request.method)
    if request.method == 'POST':
        ## 打印请求头
        # print("Request Headers:", request.headers)
        ## 打印原始请求体数据
        # raw_data = request.get_data()
        # print("Raw Request Body:", raw_data)

        # 获取输入框中的内容
        input_text = request.form['text']
        # input_text =  "帮忙写一个HA自动化yaml脚本,晚上8:00打开ID=123的灯"
        # print(input_text)

        selected_device = request.form.get('device')
        for item in ha_ws.device_data.get("result", []):
            if item.get("name") == selected_device:
                device_id = item.get("id")
        model_text = "帮忙写一个HA自动化yaml脚本,控制ID="+device_id+"的设备"+input_text
        yaml_str = get_chat_response(model_text)
        #print(yaml_str)

        # 在输出框中显示输入内容
        return jsonify({'output': yaml_str,
                        "device_items": ha_ws.device_list,
                        "selected_device": selected_device
                        })
    else:
        return render_template('index.html', 
                            device_items = ha_ws.device_list, 
                            area_items   = ha_ws.area_list,
                            label_items  = ha_ws.label_list,
                            script_items = ha_auto_cfg.auto_script_list)

@app.route('/area_operate', methods=['POST'])
def get_area_device():
    area_op = request.json.get('area_op')
    area_id = request.json.get('area_id')
    action  = request.json.get('action')

    # 执行相应的操作
    print("area op:", area_op, area_id, action)
    if area_op == 'send_device_list':
        device_list = request.json.get('device_list')
        print("area send: ", area_id, action, device_list)
        if action == 'add':
            asyncio.run(ha_ws.ha_ws_add_devices_to_area(area_id, device_list))
        else :
            asyncio.run(ha_ws.ha_ws_remove_devices_from_area(area_id, device_list))

    # 更新设备列表
    asyncio.run(ha_ws.ha_ws_get_device_list())
    # 更新区域设备列表
    if action == 'add':
        devices = ha_ws.ha_ws_get_device_not_in_area(area_id)
    else :
        devices = ha_ws.ha_ws_get_device_in_area(area_id)
    device_list = [{"name": item.get("name"), "id": item.get("id")}  for item in devices]
    print("area device: ", area_id, device_list)
    return jsonify({'device_list': device_list})
    
@app.route('/label_operate', methods=['POST'])
def get_label_device():
    label_op = request.json.get('label_op')
    label_id = request.json.get('label_id')
    action  = request.json.get('action')

    # 执行相应的操作
    print("label op:", label_op, label_id, action)
    if label_op == 'send_device_list':
        device_list = request.json.get('device_list')
        print("label send: ", label_id, action, device_list)
        if action == 'add':
            asyncio.run(ha_ws.ha_ws_add_devices_to_label(label_id, device_list))
        else :
            asyncio.run(ha_ws.ha_ws_remove_devices_from_label(label_id, device_list))

    # 更新设备列表
    asyncio.run(ha_ws.ha_ws_get_device_list())
    # 更新区域设备列表
    if action == 'add':
        devices = ha_ws.ha_ws_get_device_not_in_label(label_id)
    else :
        devices = ha_ws.ha_ws_get_device_in_label(label_id)
    device_list = [{"name": item.get("name"), "id": item.get("id")}  for item in devices]
    print("label device ", label_id, device_list)
    return jsonify({'device_list': device_list})

@app.route('/script_edit/get_orgin_script', methods=['POST'])
def get_script_text():
    script_id = request.json.get('script_id')
    print("script_id ", script_id)
    script_text = ha_auto_cfg.get_auto_script_text(script_id)

    return jsonify({'script_text': script_text})

@app.route('/script_edit/ask_modify_request', methods=['POST'])
def ask_modify_request():
    script_id   = request.json.get('script_id')
    editContent = request.json.get('editContent')
    print("script_id ", script_id)
    print("editContent ", editContent)
    script_text = ha_auto_cfg.get_auto_script_text(script_id)
    model_text = script_text + editContent
    script_text = get_chat_response(model_text)

    return jsonify({'script_text': script_text})

@app.route('/script_edit/apply_modify_script', methods=['POST'])
def apply_modify_script():
    script_id     = request.json.get('script_id')
    modifyContent = request.json.get('modifyContent')
    print("script_id ", script_id)
    print("modifyContent ", modifyContent)
    ha_auto_cfg.set_auto_script_text(script_id, modifyContent)

    script_text = ha_auto_cfg.get_auto_script_text(script_id)
    print("script_text ", script_text)
    return jsonify({'script_text': script_text})

if __name__ == '__main__':
    app.run(debug=True)
