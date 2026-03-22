import os
import requests
import json

# MemOS配置
MEMOS_API_KEY = "mpg-AIJdBtmjbN9G0XYcdpXB8ezMspF//XQ8C7GABMHD"
MEMOS_BASE_URL = "https://memos.memtensor.cn/api/openmem/v1"
USER_ID = "openclaw-user"
MEM_CUBE_ID = "default"

def add_memory(content, tags=None):
    """添加记忆到MemOS"""
    url = f"{MEMOS_BASE_URL}/add/message"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Token {MEMOS_API_KEY}"
    }
    data = {
        "user_id": USER_ID,
        "conversation_id": "history-import",
        "messages": [
            {
                "role": "user",
                "content": content
            }
        ],
        "tags": tags or ["import", "history", "memory"]
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        print(f"✅ 导入成功: {len(content)} 字符")
        return True
    except Exception as e:
        print(f"❌ 导入失败: {str(e)}")
        return False

def import_file(file_path, tags=None):
    """导入单个文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        if not content.strip():
            print(f"⏭️  跳过空文件: {file_path}")
            return True
        file_tags = tags or []
        file_tags.append(os.path.basename(file_path))
        print(f"📥 导入文件: {file_path}")
        return add_memory(content, file_tags)
    except Exception as e:
        print(f"❌ 读取文件失败 {file_path}: {str(e)}")
        return False

def import_directory(dir_path, tags=None):
    """递归导入目录下的所有.md文件"""
    success_count = 0
    total_count = 0
    
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if file.endswith('.md'):
                total_count += 1
                file_path = os.path.join(root, file)
                if import_file(file_path, tags):
                    success_count += 1
    
    return success_count, total_count

if __name__ == "__main__":
    print("🚀 开始导入历史记忆到MemOS...")
    
    # 导入核心MEMORY.md
    print("\n📌 导入核心长期记忆库 MEMORY.md...")
    import_file("/root/.openclaw/workspace/MEMORY.md", ["core", "longterm"])
    
    # 导入USER.md和SOUL.md
    print("\n👤 导入用户配置和核心规则...")
    import_file("/root/.openclaw/workspace/USER.md", ["user", "config"])
    import_file("/root/.openclaw/workspace/SOUL.md", ["config", "rules"])
    
    # 导入memory目录下的所有文件
    print("\n📂 导入memory目录下所有历史记忆...")
    success, total = import_directory("/root/.openclaw/workspace/memory/", ["history", "daily"])
    
    print(f"\n🎉 导入完成! 成功: {success}/{total}")
