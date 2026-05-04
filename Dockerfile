FROM python:3.12-slim

# 設定工作目錄
WORKDIR /app

# 避免產生 .pyc，讓 log 即時輸出
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 安裝依賴（先 copy requirements 才能利用 docker cache）
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 複製程式碼
COPY app ./app

# 啟動 FastAPI（Uvicorn）
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
