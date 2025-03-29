import os
import json
import websockets

# 替换为你的Home Assistant URL和长期访问令牌
uri = "ws://supervisor/core/websocket"
token = os.getenv('SUPERVISOR_TOKEN')

device_list_msg = {
    "id": 1,
    "type": "config/device_registry/list"
}
label_list_msg = {
    "id": 2,
    "type": "config/label_registry/list"
}
area_list_msg = {
    "id": 3,
    "type": "config/area_registry/list"
}
entity_list_msg = {
    "id": 4,
    "type": "config/entity_registry/list"
}
auto_list_msg = {
    "id": 5,
    "type": "automation/config",
    "entity_id": "automation.wan_shang_11dian_zi_dong_guan_bi_tai_deng_deng"
}

device_list = None
area_list   = None
label_list  = None
device_data = None

async def ha_ws_connect():
    # 尝试连接到Home Assistant
    websocket = await websockets.connect(uri)
    # 等待连接响应
    response = await websocket.recv()
    response_data = json.loads(response)
    #print(f"response_data message11: {response_data}")
    if response_data["type"] == "auth_required":
        # 发送认证消息
        auth_message = {
            "type": "auth",
            "access_token": token
        }
        await websocket.send(json.dumps(auth_message))
        # 等待认证响应
        response = await websocket.recv()
        response_data = json.loads(response)
        #print(f"response_data message22: {response_data}")
        if response_data["type"] != "auth_ok":
            print("Authentication failed", token, response_data)
            return None
    return websocket

async def ha_ws_get_device_list():
    websocket = await ha_ws_connect()
    if websocket is None:
        print("Failed to connect to Home Assistant")
        return

    # get device list
    send_msg = device_list_msg
    await websocket.send(json.dumps(send_msg))
    # 处理接收到的消息
    # print("bgn Received device_data")
    global device_list
    global device_data
    rsp_msg = await websocket.recv()
    device_data = json.loads(rsp_msg)
    # print("[device rsp_data:]", device_data)
    device_list = [item.get("name") for item in device_data.get("result", [])]
    # print("[device_list:]", device_list)

async def ha_ws_get_label_list():
    websocket = await ha_ws_connect()
    if websocket is None:
        print("Failed to connect to Home Assistant")
        return

    # get device list
    send_msg = label_list_msg
    # print("[label send_data:]", send_msg)
    await websocket.send(json.dumps(send_msg))
    # 处理接收到的消息
    # print("bgn Received device_data")
    global label_list
    rsp_msg = await websocket.recv()
    rsp_data = json.loads(rsp_msg)
    # print("[label rsp_data:]", rsp_data)
    label_list = [{"name": item.get("name"), "label_id": item.get("label_id")} for item in rsp_data.get("result", [])]
    # print("[label_list:]", label_list)

async def ha_ws_get_area_list():
    websocket = await ha_ws_connect()
    if websocket is None:
        print("Failed to connect to Home Assistant")
        return

    # get area list
    send_msg = area_list_msg
    await websocket.send(json.dumps(send_msg))
    # 处理接收到的消息
    global area_list
    rsp_msg = await websocket.recv()
    rsp_data = json.loads(rsp_msg)
    # print("[area rsp_data:]", rsp_data)
    area_list = [{"name": item.get("name"), "area_id": item.get("area_id")} for item in rsp_data.get("result", [])]
    # print("[area_list:]", area_list)

async def ha_ws_get_entity_list():
    websocket = await ha_ws_connect()
    if websocket is None:
        print("Failed to connect to Home Assistant")
        return

    # get area list
    send_msg = entity_list_msg
    await websocket.send(json.dumps(send_msg))
    # 处理接收到的消息
    global area_list
    rsp_msg = await websocket.recv()
    rsp_data = json.loads(rsp_msg)
    # print("[entity rsp_data:]", rsp_data)
    area_list = [{"name": item.get("name"), "area_id": item.get("area_id")} for item in rsp_data.get("result", [])]
    # print("[area_list:]", area_list)

async def ha_ws_get_auto_list():
    websocket = await ha_ws_connect()
    if websocket is None:
        print("Failed to connect to Home Assistant")
        return

    # get area list
    send_msg = auto_list_msg
    await websocket.send(json.dumps(send_msg))
    # 处理接收到的消息
    global area_list
    rsp_msg = await websocket.recv()
    rsp_data = json.loads(rsp_msg)
    # print("[auto rsp_data:]", rsp_data)
    # area_list = [{"name": item.get("name"), "area_id": item.get("area_id")} for item in rsp_data.get("result", [])]
    # print("[area_list:]", area_list)

async def ha_ws_add_devices_to_label(label_id, device_list):
    websocket = await ha_ws_connect()
    if websocket is None:
        print("Failed to connect to Home Assistant")
        return

    # add device to area
    item_no = 1
    for item in device_list:
        label_items = []
        label_items.append(label_id)
        send_msg = {
            "id"        : item_no,
            "type"      : "config/device_registry/update",
            "device_id" : item.get("id"),
            "labels"    : label_items,
        }
        item_no += 1
        await websocket.send(json.dumps(send_msg))
        # 处理接收到的消息
        # print("send update:", send_msg)
        rsp_msg = await websocket.recv()
        rsp_data = json.loads(rsp_msg)
        print("[rsp_data:]", rsp_data)

async def ha_ws_remove_devices_from_label(label_id, device_list):
    websocket = await ha_ws_connect()
    if websocket is None:
        print("Failed to connect to Home Assistant")
        return

    # del device from area
    item_no = 1
    for item in device_list:
        label_items = []
        label_items.append("")
        send_msg = {
            "id"        : item_no,
            "type"      : "config/device_registry/update",
            "device_id" : item.get("id"),
            "labels"    : label_items,
        }
        item_no += 1
        await websocket.send(json.dumps(send_msg))
        # 处理接收到的消息
        # print("send update:", send_msg)
        rsp_msg = await websocket.recv()
        rsp_data = json.loads(rsp_msg)
        # print("[rsp_data:]", rsp_data)

async def ha_ws_add_devices_to_area(area_id, device_list):
    websocket = await ha_ws_connect()
    if websocket is None:
        print("Failed to connect to Home Assistant")
        return

    # add device to area
    item_no = 1
    for item in device_list:
        send_msg = {
            "id"        : item_no,
            "type"      : "config/device_registry/update",
            "device_id" : item.get("id"),
            "area_id"   : area_id,
        }
        item_no += 1
        await websocket.send(json.dumps(send_msg))
        # 处理接收到的消息
        # print("send update:", send_msg)
        rsp_msg = await websocket.recv()
        rsp_data = json.loads(rsp_msg)
        # print("[rsp_data:]", rsp_data)

async def ha_ws_remove_devices_from_area(area_id, device_list):
    websocket = await ha_ws_connect()
    if websocket is None:
        print("Failed to connect to Home Assistant")
        return

    # del device from area
    item_no = 1
    for item in device_list:
        send_msg = {
            "id"        : item_no,
            "type"      : "config/device_registry/update",
            "device_id" : item.get("id"),
            "area_id"   : None,
        }
        item_no += 1
        await websocket.send(json.dumps(send_msg))
        # 处理接收到的消息
        # print("send update:", send_msg)
        rsp_msg = await websocket.recv()
        rsp_data = json.loads(rsp_msg)
        # print("[rsp_data:]", rsp_data)

def ha_ws_get_device_in_area(area_id):
    global device_data
    devices = [item for item in device_data.get("result", []) if str(item.get("area_id")) == area_id]
    return devices

def ha_ws_get_device_not_in_area(area_id):
    global device_data
    devices = [item for item in device_data.get("result", []) if str(item.get("area_id")) != area_id]
    return devices

def ha_ws_get_device_in_label(label_id):
    global device_data
    devices = [item for item in device_data.get("result", []) if label_id in item.get("labels", [])]
    return devices

def ha_ws_get_device_not_in_label(label_id):
    global device_data
    devices = [item for item in device_data.get("result", []) if label_id not in item.get("labels", [])]
    return devices