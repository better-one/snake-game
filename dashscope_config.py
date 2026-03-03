# 阿里云百炼 DashScope 配置
# 获取 API Key: https://bailian.console.aliyun.com/ 或 https://dashscope.console.aliyun.com/apiKey

# 重要：Coding Plan 专属 API Key（以 sk-sp- 开头）必须使用专属 API 地址
# 通用 API Key（以 sk- 开头）使用通用 API 地址

# API Key 配置
DASHSCOPE_API_KEY = "sk-sp-4c6bc141469d4ed7be788c9cb0e6af39"

# Coding Plan 专属 API 端点（用于 sk-sp- 开头的 API Key）
CODING_PLAN_BASE_URL = "https://coding.dashscope.aliyuncs.com/v1"

# 通用 DashScope API 端点（用于 sk- 开头的 API Key）
DASHSCOPE_BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"

# 根据 API Key 前缀自动选择端点
if DASHSCOPE_API_KEY.startswith("sk-sp-"):
    API_BASE_URL = CODING_PLAN_BASE_URL
    print("✓ 检测到 Coding Plan API Key，使用专属 API 端点")
else:
    API_BASE_URL = DASHSCOPE_BASE_URL
    print("✓ 检测到通用 API Key，使用通用 API 端点")

# 默认模型配置
DEFAULT_MODEL = "qwen3.5-plus"  # Coding Plan 支持 Qwen3.5-Plus 等模型

# 模型配置
MODELS = {
    "qwen3.5-plus": {
        "name": "Qwen3.5-Plus",
        "max_tokens": 8192,
        "context_window": 256000,
        "description": "通义千问 3.5 Plus 版本，性能均衡"
    },
    "qwen3.5-flash": {
        "name": "Qwen3.5-Flash",
        "max_tokens": 8192,
        "context_window": 256000,
        "description": "通义千问 3.5 Flash 版本，速度快"
    },
    "qwen3-coder": {
        "name": "Qwen3-Coder",
        "max_tokens": 8192,
        "context_window": 256000,
        "description": "通义千问 3 代码专用模型"
    }
}
