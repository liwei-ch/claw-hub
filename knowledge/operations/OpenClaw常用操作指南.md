# OpenClaw 常用操作指南
## 一、基础信息查询
### 1. 版本查询
```bash
openclaw --version
```
### 2. 运行状态查询
```bash
openclaw status
/session_status  # 会话内查询
```
### 3. 当前模型查询
通过 `/session_status` 命令查看当前使用的模型信息
---
## 二、模型管理
### 1. 临时切换模型（会话内生效）
```
/session_status model=<模型名称>
# 示例：切换到豆包Seed 2.0 Pro
/session_status model=ark/doubao-seed-2.0-pro
```
### 2. 永久修改默认模型
修改 `/root/.openclaw/openclaw.json` 配置文件：
```json
"agents": {
  "defaults": {
    "model": {
      "primary": "ark/doubao-seed-2.0-pro"  # 修改为目标模型
    }
  }
}
```
修改后重启gateway生效：`openclaw gateway restart`
---
## 三、配置管理
### 1. 超时时间配置
在 `/root/.openclaw/openclaw.json` 的 `agents.defaults` 下添加：
```json
"timeoutSeconds": 120  # 超时时间设置为120秒
```
### 2. 定时任务管理
- 查看当前定时任务：`crontab -l`
- 定时任务配置文件：`/root/.openclaw/workspace/HEARTBEAT.md`
---
## 四、服务管理
```bash
# 启动gateway
openclaw gateway start
# 停止gateway
openclaw gateway stop
# 重启gateway
openclaw gateway restart
# 查看gateway状态
openclaw gateway status
```
---
*生效时间：2026-03-14*
