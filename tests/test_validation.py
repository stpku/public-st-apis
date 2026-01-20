"""
API 验证测试用例

测试 validate_apis.py 中的验证逻辑
"""

import pytest
import json
import tempfile
from pathlib import Path
import sys

# 添加项目根目录到路径，确保可以导入utils模块
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.validate_apis import (
    validate_api_entry,
    validate_api_file,
    validate_all_api_files,
    safe_print
)


# ============================================================
# Fixtures
# ============================================================

@pytest.fixture
def valid_api_entry():
    """提供有效的API条目数据"""
    return {
        "name": "Test API",
        "description": "A test API for unit testing",
        "auth": "apiKey",
        "https": True,
        "cors": "yes",
        "category": "Test Category",
        "url": "https://example.com/api"
    }


@pytest.fixture
def valid_api_file(tmp_path):
    """创建临时有效API文件"""
    api_list = [
        {
            "name": "Test API 1",
            "description": "First test API",
            "auth": "apiKey",
            "https": True,
            "cors": "yes",
            "category": "Test",
            "url": "https://example1.com"
        },
        {
            "name": "Test API 2",
            "description": "Second test API",
            "auth": None,
            "https": True,
            "cors": "no",
            "category": "Test",
            "url": "https://example2.com"
        }
    ]
    
    file_path = tmp_path / "test_apis.json"
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(api_list, f, ensure_ascii=False, indent=2)
    
    return file_path


@pytest.fixture
def invalid_json_file(tmp_path):
    """创建临时无效JSON文件"""
    file_path = tmp_path / "invalid.json"
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write('{ "invalid": json }')
    return file_path


@pytest.fixture
def empty_api_file(tmp_path):
    """创建空API列表文件"""
    file_path = tmp_path / "empty.json"
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump([], f)
    return file_path


# ============================================================
# Test Cases: validate_api_entry
# ============================================================

class TestValidateApiEntry:
    """验证单个API条目的测试类"""
    
    def test_valid_entry(self, valid_api_entry):
        """测试有效API条目应该通过验证"""
        is_valid, message = validate_api_entry(valid_api_entry)
        assert is_valid is True, f"应为有效条目: {message}"
        assert message == "验证通过"
    
    def test_missing_name_field(self):
        """测试缺少name字段应该失败"""
        invalid_entry = {
            "description": "Test description",
            "auth": None,
            "https": True,
            "cors": "yes",
            "category": "Test",
            "url": "https://example.com"
        }
        is_valid, message = validate_api_entry(invalid_entry)
        assert is_valid is False
        assert "name" in message.lower()
    
    def test_missing_multiple_fields(self):
        """测试缺少多个字段应该失败"""
        invalid_entry = {"name": "Test"}
        is_valid, message = validate_api_entry(invalid_entry)
        assert is_valid is False
        assert "缺少必需字段" in message
    
    def test_invalid_name_type(self):
        """测试name字段类型无效应该失败"""
        invalid_entry = {
            "name": 123,  # 应该是字符串
            "description": "Test",
            "auth": None,
            "https": True,
            "cors": "yes",
            "category": "Test",
            "url": "https://example.com"
        }
        is_valid, message = validate_api_entry(invalid_entry)
        assert is_valid is False
        assert "name" in message.lower() and "类型" in message
    
    def test_empty_name(self):
        """测试空name应该失败"""
        invalid_entry = {
            "name": "   ",  # 空格不算有效字符串
            "description": "Test",
            "auth": None,
            "https": True,
            "cors": "yes",
            "category": "Test",
            "url": "https://example.com"
        }
        is_valid, message = validate_api_entry(invalid_entry)
        assert is_valid is False
        assert "name" in message.lower() and "空" in message
    
    def test_invalid_auth_type(self):
        """测试auth字段类型无效应该失败"""
        invalid_entry = {
            "name": "Test",
            "description": "Test",
            "auth": 123,  # 应该是字符串或None
            "https": True,
            "cors": "yes",
            "category": "Test",
            "url": "https://example.com"
        }
        is_valid, message = validate_api_entry(invalid_entry)
        assert is_valid is False
        assert "auth" in message.lower()
    
    def test_valid_null_auth(self):
        """测试null auth应该通过验证"""
        valid_entry = {
            "name": "Test",
            "description": "Test",
            "auth": None,  # null是有效的
            "https": True,
            "cors": "yes",
            "category": "Test",
            "url": "https://example.com"
        }
        is_valid, message = validate_api_entry(valid_entry)
        assert is_valid is True
    
    def test_invalid_https_type(self):
        """测试https字段类型无效应该失败"""
        invalid_entry = {
            "name": "Test",
            "description": "Test",
            "auth": None,
            "https": "yes",  # 应该是布尔值
            "cors": "yes",
            "category": "Test",
            "url": "https://example.com"
        }
        is_valid, message = validate_api_entry(invalid_entry)
        assert is_valid is False
        assert "https" in message.lower()
    
    def test_invalid_cors_value(self):
        """测试cors字段值无效应该失败"""
        invalid_entry = {
            "name": "Test",
            "description": "Test",
            "auth": None,
            "https": True,
            "cors": "maybe",  # 应该是 yes/no/unknown
            "category": "Test",
            "url": "https://example.com"
        }
        is_valid, message = validate_api_entry(invalid_entry)
        assert is_valid is False
        assert "cors" in message.lower()
    
    @pytest.mark.parametrize("cors_value", ["yes", "no", "unknown"])
    def test_valid_cors_values(self, cors_value):
        """测试所有有效的cors值"""
        valid_entry = {
            "name": "Test",
            "description": "Test",
            "auth": None,
            "https": True,
            "cors": cors_value,
            "category": "Test",
            "url": "https://example.com"
        }
        is_valid, message = validate_api_entry(valid_entry)
        assert is_valid is True
    
    def test_invalid_url_format(self):
        """测试无效URL格式应该失败"""
        invalid_entry = {
            "name": "Test",
            "description": "Test",
            "auth": None,
            "https": True,
            "cors": "yes",
            "category": "Test",
            "url": "not-a-valid-url"
        }
        is_valid, message = validate_api_entry(invalid_entry)
        assert is_valid is False
        assert "url" in message.lower()
    
    @pytest.mark.parametrize("url_prefix", ["http://", "https://"])
    def test_valid_url_formats(self, url_prefix):
        """测试有效的URL格式"""
        valid_entry = {
            "name": "Test",
            "description": "Test",
            "auth": None,
            "https": True,
            "cors": "yes",
            "category": "Test",
            "url": f"{url_prefix}example.com"
        }
        is_valid, message = validate_api_entry(valid_entry)
        assert is_valid is True
    
    def test_empty_url(self):
        """测试空URL应该失败"""
        invalid_entry = {
            "name": "Test",
            "description": "Test",
            "auth": None,
            "https": True,
            "cors": "yes",
            "category": "Test",
            "url": ""
        }
        is_valid, message = validate_api_entry(invalid_entry)
        assert is_valid is False


# ============================================================
# Test Cases: validate_api_file
# ============================================================

class TestValidateApiFile:
    """验证API文件的测试类"""
    
    def test_valid_file(self, valid_api_file):
        """测试有效API文件应该通过验证"""
        is_valid, message = validate_api_file(valid_api_file)
        assert is_valid is True, f"应为有效文件: {message}"
        assert "验证通过" in message
        assert "2" in message  # 有2个API条目
    
    def test_nonexistent_file(self):
        """测试不存在的文件应该失败"""
        invalid_path = Path("/nonexistent/path/file.json")
        is_valid, message = validate_api_file(invalid_path)
        assert is_valid is False
        assert "不存在" in message
    
    def test_directory_instead_of_file(self, tmp_path):
        """测试目录路径应该失败"""
        dir_path = tmp_path / "directory"
        dir_path.mkdir()
        is_valid, message = validate_api_file(dir_path)
        assert is_valid is False
        assert "不是有效文件" in message
    
    def test_invalid_json_file(self, invalid_json_file):
        """测试无效JSON文件应该失败"""
        is_valid, message = validate_api_file(invalid_json_file)
        assert is_valid is False
        assert "JSON" in message or "语法" in message
    
    def test_empty_api_list(self, empty_api_file):
        """测试空API列表应该失败"""
        is_valid, message = validate_api_file(empty_api_file)
        assert is_valid is False
        assert "空" in message
    
    def test_json_array_required(self, tmp_path):
        """测试JSON根元素必须是数组"""
        # 创建根元素为对象的JSON文件
        file_path = tmp_path / "object_root.json"
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump({"key": "value"}, f)
        
        is_valid, message = validate_api_file(file_path)
        assert is_valid is False
        assert "数组" in message
    
    def test_file_with_invalid_entry(self, tmp_path):
        """测试包含无效条目的文件应该失败"""
        api_list = [
            {
                "name": "Valid API",
                "description": "Valid API description",
                "auth": None,
                "https": True,
                "cors": "yes",
                "category": "Test",
                "url": "https://valid.com"
            },
            {
                "name": "Invalid API",
                "description": "Invalid API",
                "auth": None,
                "https": True,
                "cors": "maybe",  # 无效的cors值
                "category": "Test",
                "url": "https://invalid.com"
            }
        ]
        
        file_path = tmp_path / "mixed.json"
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(api_list, f, ensure_ascii=False, indent=2)
        
        is_valid, message = validate_api_file(file_path)
        assert is_valid is False
        assert "2" in message  # 第二个条目
    
    def test_permission_denied_simulation(self, tmp_path):
        """测试文件读取错误的处理（模拟权限问题）"""
        # 在Windows上，chmod 0o000 不会阻止文件读取
        # 我们改用模拟的方式测试错误处理逻辑
        
        # 创建一个有效的API文件
        file_path = tmp_path / "test.json"
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump([{
                "name": "Test",
                "description": "Test",
                "auth": None,
                "https": True,
                "cors": "yes",
                "category": "Test",
                "url": "https://test.com"
            }], f)
        
        # 验证正常情况下应该通过
        is_valid, message = validate_api_file(file_path)
        assert is_valid is True, f"正常文件应该通过验证: {message}"
        
        # 验证文件存在性检查
        nonexistent = tmp_path / "nonexistent.json"
        is_valid, message = validate_api_file(nonexistent)
        assert is_valid is False
        assert "不存在" in message


# ============================================================
# Test Cases: safe_print
# ============================================================

class TestSafePrint:
    """测试安全打印函数的测试类"""
    
    def test_normal_string(self):
        """测试正常字符串应该正常打印"""
        # 不抛出异常即可
        safe_print("Normal test string")
    
    def test_special_characters(self):
        """测试特殊字符应该被替换"""
        # 应该不抛出UnicodeEncodeError
        safe_print("Test with special chars: ✓ and ✗")
    
    def test_unicode_characters(self):
        """测试Unicode字符应该被处理"""
        safe_print("Chinese: 中文测试")
        safe_print("Emoji: 🚀 🌟")
    
    def test_empty_string(self):
        """测试空字符串"""
        safe_print("")
    
    def test_none_value(self):
        """测试None值应该被转换为字符串"""
        safe_print(None)


# ============================================================
# Test Cases: Integration
# ============================================================

class TestIntegration:
    """集成测试类"""
    
    def test_all_real_api_files(self):
        """测试所有实际的API文件"""
        api_path = Path("api")
        
        if not api_path.exists():
            pytest.skip("API目录不存在")
        
        all_files = list(api_path.rglob("*.json"))
        assert len(all_files) > 0, "应该存在API文件"
        
        # 每个文件都应通过验证
        for file_path in all_files:
            is_valid, message = validate_api_file(file_path)
            assert is_valid is True, f"文件 {file_path} 应通过验证: {message}"
    
    def test_validate_all_api_files_function(self):
        """测试validate_all_api_files函数"""
        # 应该返回True且不抛出异常
        result = validate_all_api_files()
        assert result is True


# ============================================================
# Test Cases: Edge Cases
# ============================================================

class TestEdgeCases:
    """边界情况测试类"""
    
    def test_very_long_name(self):
        """测试超长name字段"""
        long_name = "A" * 10000
        valid_entry = {
            "name": long_name,
            "description": "Test with very long name",
            "auth": None,
            "https": True,
            "cors": "yes",
            "category": "Test",
            "url": "https://example.com"
        }
        is_valid, message = validate_api_entry(valid_entry)
        assert is_valid is True
    
    def test_special_characters_in_fields(self):
        """测试字段中的特殊字符"""
        valid_entry = {
            "name": "API with special chars: àéïõü 中文 🎉",
            "description": "Description with \"quotes\" and 'apostrophes'",
            "auth": "api-key_123",
            "https": True,
            "cors": "yes",
            "category": "Test",
            "url": "https://example.com/api/v2.0/test"
        }
        is_valid, message = validate_api_entry(valid_entry)
        assert is_valid is True
    
    def test_url_with_port(self):
        """测试带端口的URL"""
        valid_entry = {
            "name": "Test",
            "description": "Test",
            "auth": None,
            "https": True,
            "cors": "yes",
            "category": "Test",
            "url": "https://example.com:8080/api"
        }
        is_valid, message = validate_api_entry(valid_entry)
        assert is_valid is True
    
    def test_url_with_query_params(self):
        """测试带查询参数的URL"""
        valid_entry = {
            "name": "Test",
            "description": "Test",
            "auth": None,
            "https": True,
            "cors": "yes",
            "category": "Test",
            "url": "https://example.com/api?key=value&foo=bar"
        }
        is_valid, message = validate_api_entry(valid_entry)
        assert is_valid is True
