# OpenClaw 标准升级流程
## 🔒 强制规范，所有升级必须严格遵循
### 一、升级前操作（必须完成）
#### 1. 核心数据备份
创建带当前日期的备份文件夹，复制以下核心内容：
```bash
# 创建备份目录
BACKUP_DIR="/root/.openclaw/upgrade_backup/$(date +%Y%m%d_%H%M%S)"
mkdir -p $BACKUP_DIR
# 备份核心数据
cp -r /root/.openclaw/workspace/memory $BACKUP_DIR/
cp -r /root/.openclaw/workspace/skills $BACKUP_DIR/
cp /root/.openclaw/openclaw.json $BACKUP_DIR/config.yaml
# 验证备份完整性
ls -la $BACKUP_DIR/
```
#### 2. 状态信息采集
生成 `UPGRADE_README.md` 存入 `memory/` 目录，包含以下内容：
- 当前运行版本号
- 正在运行的所有心跳/定时任务列表
- 核心长期记忆路径
- 常用技能列表
- 当前配置的核心参数
---
### 二、升级执行
1. 执行升级命令：`npm update -g openclaw`
2. 验证升级成功：`openclaw --version`
3. 重启gateway服务：`openclaw gateway restart`
4. 等待服务启动完成，验证基本功能正常
---
### 三、升级后验证
1. 读取 `memory/UPGRADE_README.md`
2. 确认身份和核心配置未发生变化
3. 验证所有心跳/定时任务正常运行
4. 确认核心记忆和技能完整可用
5. 向用户报告升级完成状态
---
### 四、版本历史记录
每次升级后在 `memory/upgrade_history.md` 中记录：
- 升级前版本 → 升级后版本
- 升级时间
- 备份目录路径
- 升级过程中遇到的问题和解决方法
---
*生效时间：2026-03-14*
