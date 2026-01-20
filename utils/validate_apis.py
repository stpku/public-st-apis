"""
API 数据验证工具

此脚本用于验证 API 数据文件的格式是否符合规范
支持跨平台运行（Windows/Linux/macOS）
"""

import json
import sys
from pathlib import Path
from typing import Tuple, Optional


# ============================================================
# 编码兼容层
# ============================================================

def setup_encoding():
    """设置正确的编码输出，解决Windows GBK编码问题"""
    if sys.platform == 'win32':
        # Windows控制台默认使用GBK编码，不支持特殊Unicode字符
        # 使用降级方案：自定义safe_print处理特殊字符
        pass


def safe_print(*args, **kwargs):
    """
    安全打印函数，自动处理编码问题
    - Windows: 将特殊Unicode字符替换为ASCII兼容版本
    - Linux/macOS: 正常输出
    """
    # 转换特殊字符
    processed_args = []
    for arg in args:
        if isinstance(arg, str):
            # 替换特殊Unicode字符为ASCII兼容版本
            arg = arg.replace('✓', '[PASS]')
            arg = arg.replace('✗', '[FAIL]')
        processed_args.append(arg)
    
    try:
        print(*processed_args, **kwargs)
    except UnicodeEncodeError:
        # 如果仍然遇到编码错误，强制转换为ASCII
        ascii_args = [str(arg).encode('ascii', errors='replace').decode('ascii') 
                      for arg in processed_args]
        print(*ascii_args, **kwargs)


# ============================================================
# 增强的错误处理
# ============================================================

class APIValidationError(Exception):
    """API验证错误基类"""
    def __init__(self, message: str, file_path: Optional[Path] = None, 
                 line_number: Optional[int] = None):
        self.message = message
        self.file_path = file_path
        self.line_number = line_number
        super().__init__(self._format_message())
    
    def _format_message(self) -> str:
        """格式化错误消息"""
        parts = [self.message]
        if self.file_path:
            parts.append(f"文件: {self.file_path}")
        if self.line_number:
            parts.append(f"行号: {self.line_number}")
        return " | ".join(parts)


class MissingRequiredFieldError(APIValidationError):
    """缺少必需字段错误"""
    pass


class InvalidFieldTypeError(APIValidationError):
    """字段类型无效错误"""
    pass


class InvalidURLError(APIValidationError):
    """URL格式无效错误"""
    pass


class InvalidJSONError(APIValidationError):
    """JSON格式无效错误"""
    pass


class FileAccessError(APIValidationError):
    """文件访问错误"""
    pass


# ============================================================
# 验证逻辑
# ============================================================

def validate_api_entry(api_entry: dict) -> Tuple[bool, str]:
    """
    验证单个API条目的格式
    
    Args:
        api_entry: API条目字典
        
    Returns:
        (是否有效, 消息)
    """
    required_fields = ['name', 'description', 'auth', 'https', 'cors', 'category', 'url']
    
    # 1. 检查必需字段
    for field in required_fields:
        if field not in api_entry:
            return False, f"缺少必需字段: {field}"
    
    # 2. 验证字段类型 - name
    if not isinstance(api_entry['name'], str):
        return False, f"name 字段类型无效: expected str, got {type(api_entry['name']).__name__}"
    if not api_entry['name'].strip():
        return False, "name 字段不能为空"
    
    # 3. 验证字段类型 - description
    if not isinstance(api_entry['description'], str):
        return False, f"description 字段类型无效: expected str, got {type(api_entry['description']).__name__}"
    if not api_entry['description'].strip():
        return False, "description 字段不能为空"
    
    # 4. 验证字段类型 - auth
    if api_entry['auth'] is not None and not isinstance(api_entry['auth'], str):
        return False, f"auth 字段类型无效: expected str or null, got {type(api_entry['auth']).__name__}"
    
    # 5. 验证字段类型 - https
    if not isinstance(api_entry['https'], bool):
        return False, f"https 字段类型无效: expected bool, got {type(api_entry['https']).__name__}"
    
    # 6. 验证字段类型 - cors
    if api_entry['cors'] not in ['yes', 'no', 'unknown']:
        return False, f"cors 字段值无效: expected 'yes', 'no', or 'unknown', got '{api_entry['cors']}'"
    
    # 7. 验证字段类型 - category
    if not isinstance(api_entry['category'], str):
        return False, f"category 字段类型无效: expected str, got {type(api_entry['category']).__name__}"
    if not api_entry['category'].strip():
        return False, "category 字段不能为空"
    
    # 8. 验证字段类型 - url
    if not isinstance(api_entry['url'], str):
        return False, f"url 字段类型无效: expected str, got {type(api_entry['url']).__name__}"
    if not api_entry['url'].strip():
        return False, "url 字段不能为空"
    
    # 9. 验证URL格式
    url = api_entry['url'].strip()
    if not url.startswith(('http://', 'https://')):
        return False, f"url 字段格式无效: 必须以 'http://' 或 'https://' 开头"
    
    # 10. 可选：验证URL可访问性（基础检查）
    # 注意：此检查可能较慢，默认不启用
    # if not _is_url_accessible(url):
    #     return False, f"url 可能不可访问: {url}"
    
    return True, "验证通过"


def _get_json_error_line(content: str, error: json.JSONDecodeError) -> int:
    """
    获取JSON解析错误发生的行号
    
    Args:
        content: JSON文件内容
        error: JSON解析错误
        
    Returns:
        行号
    """
    return content[:error.pos].count('\n') + 1


def validate_api_file(file_path: Path) -> Tuple[bool, str]:
    """
    验证API数据文件
    
    Args:
        file_path: JSON文件路径
        
    Returns:
        (是否有效, 消息)
    """
    # 1. 检查文件存在性
    if not file_path.exists():
        return False, f"文件不存在: {file_path}"
    
    if not file_path.is_file():
        return False, f"不是有效文件: {file_path}"
    
    # 2. 检查文件扩展名
    if file_path.suffix.lower() != '.json':
        return False, f"文件扩展名无效: expected .json, got {file_path.suffix}"
    
    # 3. 读取文件内容
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except PermissionError:
        return False, f"无文件读取权限: {file_path}"
    except UnicodeDecodeError:
        return False, f"文件编码错误（非UTF-8）: {file_path}"
    except IOError as e:
        return False, f"文件读取错误: {e}"
    
    # 4. 解析JSON
    try:
        data = json.loads(content)
    except json.JSONDecodeError as e:
        line_num = _get_json_error_line(content, e)
        return False, f"JSON语法错误 (第{line_num}行): {str(e)}"
    
    # 5. 验证数据结构
    if not isinstance(data, list):
        return False, f"JSON根元素必须是数组，当前类型: {type(data).__name__}"
    
    if len(data) == 0:
        return False, f"API列表为空: {file_path}"
    
    # 6. 逐条验证API
    error_count = 0
    max_errors = 5  # 限制最大错误数量，避免输出过长
    
    for i, entry in enumerate(data):
        is_valid, message = validate_api_entry(entry)
        if not is_valid:
            error_count += 1
            if error_count == 1:
                # 第一个错误详细报告
                return False, f"第 {i+1} 个API条目验证失败: {message}"
            elif error_count >= max_errors:
                # 达到最大错误数量，停止报告
                return False, f"发现 {error_count}+ 个错误 (共 {len(data)} 条目)，停止检查"
    
    # 7. 验证通过
    return True, f"{file_path} 验证通过，共 {len(data)} 个API条目"


def validate_all_api_files(api_dir: str = "api") -> bool:
    """
    验证所有API数据文件
    
    Args:
        api_dir: API目录路径
        
    Returns:
        所有文件是否有效
    """
    api_path = Path(api_dir)
    
    # 1. 检查目录存在性
    if not api_path.exists():
        safe_print(f"[ERROR] API目录不存在: {api_path}")
        return False
    
    if not api_path.is_dir():
        safe_print(f"[ERROR] 路径不是目录: {api_path}")
        return False
    
    # 2. 查找所有JSON文件
    all_files = list(api_path.rglob("*.json"))
    
    if not all_files:
        safe_print(f"[WARN] 未找到任何JSON文件在: {api_path}")
        return False
    
    safe_print(f"[INFO] 找到 {len(all_files)} 个API数据文件")
    safe_print("-" * 60)
    
    # 3. 验证每个文件
    all_valid = True
    valid_count = 0
    invalid_count = 0
    
    for file_path in sorted(all_files):
        is_valid, message = validate_api_file(file_path)
        if is_valid:
            safe_print(f"[PASS] {message}")
            valid_count += 1
        else:
            safe_print(f"[FAIL] {message}")
            invalid_count += 1
            all_valid = False
    
    # 4. 输出汇总
    safe_print("-" * 60)
    safe_print(f"[SUMMARY] 验证完成: {valid_count} 成功, {invalid_count} 失败")
    
    return all_valid


# ============================================================
# 导出功能
# ============================================================

def export_invalid_apis(output_file: str = "validation_errors.json") -> dict:
    """
    导出验证失败的API信息到JSON文件
    
    Args:
        output_file: 输出文件名
        
    Returns:
        验证结果字典
    """
    api_path = Path("api")
    all_files = list(api_path.rglob("*.json"))
    
    results = {
        "timestamp": str(Path(__file__).stat().st_mtime),
        "total_files": len(all_files),
        "errors": [],
        "warnings": []
    }
    
    for file_path in all_files:
        is_valid, message = validate_api_file(file_path)
        if not is_valid:
            results["errors"].append({
                "file": str(file_path),
                "message": message
            })
    
    # 写入输出文件
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    return results


# ============================================================
# 入口点
# ============================================================

if __name__ == "__main__":
    # 设置编码
    setup_encoding()
    
    safe_print("=" * 60)
    safe_print("Public ST APIs 数据验证工具")
    safe_print("=" * 60)
    safe_print()
    
    # 执行验证
    success = validate_all_api_files()
    
    # 输出结果
    safe_print()
    if success:
        safe_print("[SUCCESS] 所有API数据文件验证通过！")
        sys.exit(0)
    else:
        safe_print("[FAILED] 部分API数据文件验证失败，请检查错误信息。")
        safe_print()
        safe_print("提示: 使用 'python utils/validate_apis.py --export' 导出错误报告")
        sys.exit(1)
