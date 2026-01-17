"""
API 数据验证工具

此脚本用于验证 API 数据文件的格式是否符合规范
"""

import json
import os
from pathlib import Path


def validate_api_entry(api_entry):
    """验证单个API条目的格式"""
    required_fields = ['name', 'description', 'auth', 'https', 'cors', 'category', 'url']
    
    for field in required_fields:
        if field not in api_entry:
            return False, f"缺少必需字段: {field}"
    
    # 验证字段类型
    if not isinstance(api_entry['name'], str):
        return False, "name 字段必须是字符串"
    
    if not isinstance(api_entry['description'], str):
        return False, "description 字段必须是字符串"
    
    if api_entry['auth'] is not None and not isinstance(api_entry['auth'], str):
        return False, "auth 字段必须是字符串或 null"
    
    if not isinstance(api_entry['https'], bool):
        return False, "https 字段必须是布尔值"
    
    if api_entry['cors'] not in ['yes', 'no', 'unknown']:
        return False, "cors 字段必须是 'yes', 'no', 或 'unknown'"
    
    if not isinstance(api_entry['category'], str):
        return False, "category 字段必须是字符串"
    
    if not isinstance(api_entry['url'], str):
        return False, "url 字段必须是字符串"
    
    # 验证URL格式（简单检查）
    if not api_entry['url'].startswith(('http://', 'https://')):
        return False, "url 字段必须是有效的URL"
    
    return True, "验证通过"


def validate_api_file(file_path):
    """验证API数据文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if not isinstance(data, list):
            return False, "文件内容必须是数组"
        
        for i, entry in enumerate(data):
            is_valid, message = validate_api_entry(entry)
            if not is_valid:
                return False, f"第 {i+1} 个API条目验证失败: {message}"
        
        return True, f"文件 {file_path} 验证通过，共 {len(data)} 个API条目"
    
    except json.JSONDecodeError as e:
        return False, f"JSON解析错误: {e}"
    except Exception as e:
        return False, f"文件读取错误: {e}"


def validate_all_api_files():
    """验证所有API数据文件"""
    api_dir = Path("api")
    all_files = list(api_dir.rglob("*.json"))
    
    print(f"找到 {len(all_files)} 个API数据文件")
    
    all_valid = True
    for file_path in all_files:
        is_valid, message = validate_api_file(file_path)
        if is_valid:
            print(f"✓ {message}")
        else:
            print(f"✗ {message}")
            all_valid = False
    
    return all_valid


if __name__ == "__main__":
    print("开始验证API数据文件...")
    success = validate_all_api_files()
    
    if success:
        print("\n所有API数据文件验证通过！")
    else:
        print("\n部分API数据文件验证失败，请检查错误信息。")