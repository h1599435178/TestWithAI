--
name: cron
description: 通过 test_with_ai 命令管理定时任务 - 创建、查询、暂停、恢复、删除任-
metadata: { "test_with_ai": { "emoji": "- } }
--

# 定时任务管理

使用 `test_with_ai cron` 命令管理定时任务-

## 常用命令

```bash
# 列出所有任-
test_with_ai cron list

# 查看任务详情
test_with_ai cron get <job_id>

# 查看任务状-
test_with_ai cron state <job_id>

# 删除任务
test_with_ai cron delete <job_id>

# 暂停/恢复任务
test_with_ai cron pause <job_id>
test_with_ai cron resume <job_id>

# 立即执行一-
test_with_ai cron run <job_id>
```

## 创建任务

支持两种任务类型-
- **text**：定时向频道发送固定消-
- **agent**：定时向 Agent 提问并发送回复到频道

### 快速创-

```bash
# 每天 9:00 发送文本消-
test_with_ai cron create \
  -type text \
  -name "每日早安" \
  -cron "0 9 * * *" \
  -channel imessage \
  -target-user "CHANGEME" \
  -target-session "CHANGEME" \
  -text "早上好！"

# -2 小时-Agent 提问
test_with_ai cron create \
  -type agent \
  -name "检查待- \
  -cron "0 */2 * * *" \
  -channel dingtalk \
  -target-user "CHANGEME" \
  -target-session "CHANGEME" \
  -text "我有什么待办事项？"
```

### 必填参数

创建任务需要：
- `-type`：任务类型（text -agent-
- `-name`：任务名-
- `-cron`：cron 表达式（-`"0 9 * * *"` 表示每天 9:00-
- `-channel`：目标频道（imessage / discord / dingtalk / qq / console-
- `-target-user`：用户标-
- `-target-session`：会话标-
- `-text`：消息内容（text 类型）或提问内容（agent 类型-

### -JSON 创建（复杂配置）

```bash
test_with_ai cron create -f job_spec.json
```

## Cron 表达式示-

```
0 9 * * *      # 每天 9:00
0 */2 * * *    # -2 小时
30 8 * * 1-5   # 工作-8:30
0 0 * * 0      # 每周日零-
*/15 * * * *   # -15 分钟
```

## 使用建议

- 缺少参数时，询问用户补充后再创建
- 暂停/删除/恢复前，-`test_with_ai cron list` 查找 job_id
- 排查问题时，-`test_with_ai cron state <job_id>` 查看状-
- 给用户的命令要完整、可直接复制执行
