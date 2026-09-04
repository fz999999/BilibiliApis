FROM python:3.12-slim

WORKDIR /app

# 安装系统依赖及 Node.js（execjs 需要 Node 运行时执行 JS 签名计算）
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    gnupg \
    build-essential \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y --no-install-recommends nodejs \
    && apt-get purge -y --auto-remove build-essential \
    && rm -rf /var/lib/apt/lists/*

# 先复制依赖文件，利用 Docker 层缓存
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目代码
COPY . .

# 创建非 root 用户运行服务
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 5008

ENV PYTHONUNBUFFERED=1
ENV NODE_ENV=production

HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:5008/docs || exit 1

CMD ["python", "App.py"]
