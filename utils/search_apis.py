"""
API 搜索工具

此脚本允许用户搜索特定的API或按分类浏览API
"""

import json
import os
from pathlib import Path


def load_all_apis():
    """加载所有API数据"""
    api_dir = Path("api")
    all_apis = []
    
    for json_file in api_dir.rglob("*.json"):
        with open(json_file, 'r', encoding='utf-8') as f:
            apis = json.load(f)
            # 添加文件来源信息
            for api in apis:
                api['source_file'] = str(json_file)
            all_apis.extend(apis)
    
    return all_apis


def search_apis(query, apis):
    """根据查询词搜索API"""
    query = query.lower()
    results = []
    
    for api in apis:
        if (query in api['name'].lower() or 
            query in api['description'].lower() or 
            query in api['category'].lower()):
            results.append(api)
    
    return results


def filter_by_category(category, apis):
    """按分类过滤API"""
    category = category.lower()
    results = []
    
    for api in apis:
        if category in api['category'].lower():
            results.append(api)
    
    return results


def display_api(api):
    """显示API详细信息"""
    print(f"\n名称: {api['name']}")
    print(f"描述: {api['description']}")
    print(f"认证: {api['auth'] or 'None'}")
    print(f"HTTPS: {'Yes' if api['https'] else 'No'}")
    print(f"CORS: {api['cors']}")
    print(f"分类: {api['category']}")
    print(f"URL: {api['url']}")
    if 'comment' in api:
        print(f"备注: {api['comment']}")
    print("-" * 50)


def main():
    print("Public ST APIs 搜索工具")
    print("=" * 30)
    
    # 加载所有API
    all_apis = load_all_apis()
    print(f"已加载 {len(all_apis)} 个API")
    
    while True:
        print("\n请选择操作:")
        print("1. 搜索API")
        print("2. 按分类浏览")
        print("3. 显示所有分类")
        print("4. 退出")
        
        choice = input("\n输入选择 (1-4): ").strip()
        
        if choice == '1':
            query = input("输入搜索词: ").strip()
            if query:
                results = search_apis(query, all_apis)
                print(f"\n找到 {len(results)} 个匹配的API:")
                
                for api in results:
                    display_api(api)
        
        elif choice == '2':
            print("\n可用分类:")
            categories = set(api['category'] for api in all_apis)
            for i, cat in enumerate(sorted(categories), 1):
                print(f"{i}. {cat}")
            
            cat_choice = input("\n选择分类编号: ").strip()
            try:
                cat_num = int(cat_choice) - 1
                selected_cat = sorted(categories)[cat_num]
                
                results = filter_by_category(selected_cat, all_apis)
                print(f"\n分类 '{selected_cat}' 下的 {len(results)} 个API:")
                
                for api in results:
                    display_api(api)
                    
            except (ValueError, IndexError):
                print("无效的选择")
        
        elif choice == '3':
            print("\n所有API分类:")
            categories = set(api['category'] for api in all_apis)
            for cat in sorted(categories):
                count = sum(1 for api in all_apis if api['category'] == cat)
                print(f"- {cat}: {count} 个API")
        
        elif choice == '4':
            print("再见!")
            break
        
        else:
            print("无效选择，请重试")


if __name__ == "__main__":
    main()