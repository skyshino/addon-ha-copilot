import os
import json
import yaml
import hashlib

auto_script_list = []

# 使用更复杂的密钥生成方式
def read_key(text, password):
    text = bytes.fromhex(text.split(": ")[1].strip())
    # 通过哈希生成固定长度密钥
    key = hashlib.sha256(password.encode()).digest()
    # 处理不同输入类型（字符串/字节）
    text_bytes = text.encode() if isinstance(text, str) else text
    # 重复密钥到足够长度
    extended_key = (key * (len(text_bytes) // len(key) + 1))[:len(text_bytes)]
    return bytes([b ^ k for b, k in zip(text_bytes, extended_key)])

def traverse_directory(base_path, depth=3, current_depth=0):
    if current_depth > depth:
        return
    for item in os.listdir(base_path):
        item_path = os.path.join(base_path, item)
        if os.path.isdir(item_path):
            print(f"目录: {item_path}")
            traverse_directory(item_path, depth, current_depth + 1)
        #else:
        #    print(f"文件: {item_path}")

def copy_directory(src, dst):
    try:
        # 确保目标目录存在
        os.makedirs(dst, exist_ok=True)

        # 遍历源目录中的所有文件和子目录
        for item in os.listdir(src):
            s = os.path.join(src, item)
            d = os.path.join(dst, item)
            if os.path.isdir(s):
                # 递归复制子目录
                copy_directory(s, d)
            else:
                # 复制文件
                with open(s, 'rb') as f_src:
                    with open(d, 'wb') as f_dst:
                        f_dst.write(f_src.read())

        print(f"Directory '{src}' copied to '{dst}' successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

def print_cfg_auto_yaml():
    # 打开文件
    print("configuration.yaml ::")
    with open('/homeassistant/configuration.yaml', 'r') as file:
        # 读取文件内容
        content = file.read()
        # 打印文件内容
        print(content)
    print("automations.yaml ::")
    with open('/homeassistant/automations.yaml', 'r') as file:
        # 读取文件内容
        content = file.read()
        # 打印文件内容
        print(content)

    # 将数据转换为按 id 索引的字典，并将 id 之外的部分作为文本处理
    with open('/homeassistant/automations.yaml', 'r') as file:
        data = yaml.safe_load(file)
    # 将数据转换为按 id 索引的字典，并将 id 之外的部分作为文本处理
    data_by_id = {}
    for item in data:
        id = item['id']
        # 创建一个新的字典，不包含 id
        item_without_id = {key: value for key, value in item.items() if key != 'id'}
        # 将新的字典转换为 YAML 格式的字符串
        text = yaml.dump(item_without_id, default_flow_style=False, allow_unicode=True, sort_keys=False)
        # 将 id 和文本存储到字典中
        data_by_id[id] = text
    # 打印按 id 索引的数据
    for id, text in data_by_id.items():
        print(f"ID: {id}")
        print(f"Text: \n{text}")
        print()

def get_auto_script_list():
    global auto_script_list
    # 清空列表避免重复追加
    auto_script_list.clear()
    
    # 将数据转换为按 id 索引的字典，并将 id 之外的部分作为文本处理
    with open('/homeassistant/automations.yaml', 'r') as file:
        data = yaml.safe_load(file)
    # 将数据转换为按 id 索引的字典，并将 id 之外的部分作为文本处理
    for item in data:
        id = item['id']
        alias = item['alias']
        # 创建一个新的字典，不包含 id
        item_without_id = {key: value for key, value in item.items() if key != 'id'}
        # 将新的字典转换为 YAML 格式的字符串
        text = yaml.dump(item_without_id, default_flow_style=False, allow_unicode=True, sort_keys=False)
        # 将 id 和文本存储到字典中
        script = {
            "id"    : id,
            "alias" : alias,
            "text"  : text
        }
        auto_script_list.append(script)

    # print(f"auto script list:\n{auto_script_list}")

def get_auto_script_text(script_id):
    # 将数据转换为按 id 索引的字典，并将 id 之外的部分作为文本处理
    script = None
    for item in auto_script_list:
        if str(item.get("id")) == script_id:
            script = item
            break
    # print(f"script is: {script}")
    return script["text"]

def set_auto_script_text(script_id, modifyContent):
    script = None
    # modifyContent 保存到 auto_script_list
    for item in auto_script_list:
        if str(item.get("id")) == script_id:
            item["text"] = modifyContent
            break

    # 将 auto_script_list 的 text 转换成yaml格式
    converted_list = []
    for item in auto_script_list:
        try:
            # 添加YAML解析验证
            parsed_content = yaml.safe_load(item.get("text"))
            if not isinstance(parsed_content, dict):
                raise ValueError("内容必须为字典结构")
            
            # 验证必要字段
            if 'triggers' not in parsed_content or 'actions' not in parsed_content:
                raise ValueError("YAML必须包含trigger和action字段")

            # 将text转换为字典并合并到顶层
            converted_item = {
                "id": item["id"],
                **parsed_content
            }
            converted_list.append(converted_item)
        except yaml.YAMLError as e:
            print(f"YAML解析错误 ID {script['id']}: {str(e)}")

    # 将 auto_script_list 除了 alias 外保存到 automations.yaml
    with open('/homeassistant/automations.yaml', 'w') as file:
        # 使用完整的converted_list覆盖文件
        yaml.dump(
            converted_list, 
            file,
            default_flow_style=False,
            allow_unicode=True,
            sort_keys=False
        )

    # 刷新auto_script_list
    get_auto_script_list()
    return True