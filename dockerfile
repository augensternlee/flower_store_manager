# 基础镜像
FROM python:3.9-slim-buster

# 设置工作目录
WORKDIR /app

# 安装依赖
RUN apt-get update && \
    apt-get install -y nginx && \
    pip install --upgrade pip && \
    pip install gunicorn

# 复制应用程序代码
COPY . .

# 安装应用程序依赖
RUN pip install -r requirements.txt

# 配置 Nginx
COPY nginx.conf /etc/nginx/sites-available/default

# 将端口暴露到容器外部
EXPOSE 80

# 启动命令
CMD service nginx start && gunicorn myapp.wsgi:application --bind 0.0.0.0:8000
