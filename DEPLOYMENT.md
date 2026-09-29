# Thông Tin Deploy — Checkpoint 5

> Điền file này sau khi deploy xong. `pytest tests/test_cp5.py` đọc file này
> để tìm địa chỉ service của bạn và gọi thử.
>
> **Chỉ ghi TÊN biến môi trường, tuyệt đối không dán giá trị API key vào đây.**
> Repo này công khai — dán khóa vào là mất khóa.

## Thông Tin Học Viên

| Mục | Nội dung |
|-----|----------|
| Họ và tên | Bùi Văn Quang |
| Mã học viên | 2A202602688 |
| Repo | https://github.com/Quang20040/K4-L3B-DAY12-BuiVanQuang-2A202602688-CloudServicesAndDeployment |

## Service

| Mục | Nội dung |
|-----|----------|
| Public URL | https://day12-agent-76m3.onrender.com |
| Platform | Render |
| Ngày deploy | 2026-09-29 |

## Biến Môi Trường Đã Set Trên Cloud

Ghi tên biến và **nguồn giá trị**, không ghi giá trị:

| Biến | Đã set | Ghi chú |
|------|--------|---------|
| `PORT` | ✅ | platform tự gán |
| `AGENT_API_KEY` | ✅ | đặt trong dashboard / blueprint env, không nằm trong repo |
| `REDIS_URL` | ✅ | liên kết tự động từ Render Key Value Redis (`fromService`) |
| `RATE_LIMIT_PER_MINUTE` | ✅ | 10 |
| `MONTHLY_BUDGET_USD` | ✅ | 10.0 |
| `LOG_LEVEL` | ✅ | INFO |

## Lệnh Kiểm Tra

Thay `<URL>` bằng Public URL ở trên:

```bash
# 1. Liveness — mong đợi 200 {"status":"ok"}
curl -i https://day12-agent-76m3.onrender.com/health

# 2. Readiness — mong đợi 200 {"status":"ready"} (đã nối được Redis)
curl -i https://day12-agent-76m3.onrender.com/ready

# 3. Không có API key — mong đợi 401
curl -i -X POST https://day12-agent-76m3.onrender.com/ask \
  -H "Content-Type: application/json" \
  -d '{"question":"Hello"}'

# 4. Có API key — mong đợi 200 kèm câu trả lời
curl -i -X POST https://day12-agent-76m3.onrender.com/ask \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $AGENT_API_KEY" \
  -H "X-User-Id: sv-test" \
  -d '{"question":"Deploy là gì?"}'

# 5. Rate limit — gọi 15 lần, những lần cuối phải trả 429
for i in $(seq 1 15); do
  curl -s -o /dev/null -w "%{http_code} " -X POST https://day12-agent-76m3.onrender.com/ask \
    -H "Content-Type: application/json" \
    -H "X-API-Key: $AGENT_API_KEY" \
    -H "X-User-Id: sv-test" \
    -d '{"question":"test"}'
done; echo
```

## Kết Quả Chạy Thật

Dán output của các lệnh trên vào đây:

```text
# 1. /health
HTTP/1.1 200 OK
Date: Tue, 29 Sep 2026 04:45:25 GMT
Content-Type: application/json
Connection: keep-alive
Server: cloudflare
x-render-origin-server: uvicorn

{"status":"ok","service":"day12-agent","version":"1.0.0"}

# 2. /ready
HTTP/1.1 200 OK
Date: Tue, 29 Sep 2026 04:45:37 GMT
Content-Type: application/json
Connection: keep-alive
Server: cloudflare
x-render-origin-server: uvicorn

{"status":"ready","redis":true}

# 3. /ask không có key
HTTP/1.1 401 Unauthorized
Content-Type: application/json

{"detail":"invalid or missing API key"}

# 4. /ask có key
HTTP/1.1 200 OK
Content-Type: application/json

{
  "answer": "Ngắn gọn: Deploy la gi phụ thuộc vào ba yếu tố — cấu hình qua biến môi trường, health check để orchestrator biết trạng thái, và giới hạn tài nguyên. (Mình đang nhớ 2 lượt trao đổi trước đó.)",
  "user_id": "sv-test",
  "history_length": 2,
  "cost_usd": 3.465e-05,
  "tokens": {"in": 43, "out": 47}
}

# 5. Rate limit 15 lần
200 200 200 200 200 200 200 200 200 429 429 429 429 429 429
```

## Ảnh Chụp Màn Hình

Đã lưu ảnh trong thư mục `screenshots/`:

- `screenshots/dashboard.png` — trang quản lý service trên Render
- `screenshots/health.png` — kết quả gọi `/health` trả về status 200 OK
- `screenshots/ready.png` — kết quả gọi `/ready` trả về status 200 OK (Redis ready)
- `screenshots/docs.png` — giao diện Swagger UI (/docs) trên Render
- `screenshots/ds.png` — tổng quan dashboard dịch vụ trên Render
- `screenshots/log.png` — nhật ký log hoạt động của service trên Render
- `screenshots/logd.png` — chi tiết log triển khai và runtime trên Render
