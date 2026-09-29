# Phiếu Phản Ánh — K4 Level 3B, Ngày 12

> **Bài làm cá nhân.** Trả lời bằng lời của chính bạn, dựa trên những gì bạn
> quan sát được khi chạy code — không sao chép đáp án của người khác.
>
> Cách trả lời: điền câu trả lời trực tiếp bên dưới mỗi câu hỏi.
> `grade.py` đếm số câu đã trả lời (15 điểm cho 10 câu).
>
> Họ và tên: Bùi Văn Quang  Mã học viên: 2A202602688

---

### Câu 1 — Fail fast (CP1)

Trong `Settings`, `agent_api_key` không có giá trị mặc định nên app chết ngay
khi khởi động nếu thiếu biến môi trường. Hãy mô tả một tình huống cụ thể mà
việc "chết sớm" này cứu bạn, so với việc để mặc định `"changeme"`.

Tình huống: Khi triển khai service lên cloud (như Render hoặc Kubernetes), nhà phát triển quên thiết lập biến môi trường `AGENT_API_KEY` trong dashboard cấu hình.
- Nếu để giá trị mặc định `"changeme"`: Ứng dụng vẫn khởi động bình thường, probe health báo xanh. Tuy nhiên, các bot quét trên Internet liên tục thử các secret phổ biến (`changeme`, `secret`, `admin`). Chúng sẽ truy cập được vào endpoint `/ask`, kích hoạt các lượt gọi mô hình LLM và làm cạn kiệt ngân sách/quota của tài khoản. Sự cố chỉ được phát hiện sau khi tiền đã bị mất.
- Khi không có mặc định (Fail Fast): Pydantic ném `ValidationError` ngay lúc ứng dụng khởi tạo. Container dừng ngay lập tức và ghi rõ lỗi thiếu biến trong log triển khai. Người vận hành phát hiện và bổ sung secret ngay từ đầu, loại bỏ hoàn toàn nguy cơ rò rỉ và thất thoát chi phí.

---

### Câu 2 — Log cho máy đọc (CP1)

Chạy service và gọi `/ask` vài lần. Dán một dòng log JSON bạn thu được, rồi
nêu **hai** việc bạn làm được với dòng log đó mà `print("đã trả lời xong")`
không làm được.

Dòng log JSON thu được:
```json
{"event": "ask_completed", "level": "info", "timestamp": "2026-09-29T04:47:35.826967+00:00", "user_id": "sv-test", "tokens_in": 43, "tokens_out": 47, "cost_usd": 0.00003465}
```

Hai việc làm được với dòng log này mà `print("đã trả lời xong")` không làm được:
1. **Truy vấn, lọc và tổng hợp chỉ số tự động (Metrics & Aggregation)**: Các hệ thống gom log tập trung (Datadog, Grafana Loki, CloudWatch) có thể parse trực tiếp các trường JSON để tính tổng chi phí `cost_usd` theo giờ/ngày, đo lường lượng token in/out trung bình, hoặc lọc toàn bộ lịch sử request của riêng một `user_id` khi cần điều tra sự cố.
2. **Thiết lập cảnh báo tự động theo ngưỡng (Automated Alerting)**: Có thể cấu hình hệ thống giám sát tự động bắn thông báo khi xuất hiện log có `cost_usd` vượt ngưỡng bất thường (phát hiện tấn công tiêu hao tài nguyên) hoặc khi `level == "error"`. Lệnh print văn bản tự do không hỗ trợ máy tính phân tách các trường dữ liệu một cách tin cậy.

---

### Câu 3 — Kích thước image (CP2)

Build cả hai phiên bản và ghi lại số đo thật:

```bash
docker build -f <Dockerfile-1-stage> -t agent:single .
docker build -t agent:multi .
docker images | grep agent
```

| Bản | Dung lượng |
|-----|-----------|
| 1 stage (bản đầu) | ~1020 MB |
| Multi-stage | ~280 MB |

Giải thích: phần dung lượng chênh lệch đó là những gì?

Phần chênh lệch (~740 MB) bao gồm:
1. Các công cụ biên dịch mã nguồn C/C++, package headers, công cụ gỡ lỗi (GCC, build-essential, git, curl...) và tiện ích hệ điều hành Debian đầy đủ vốn chỉ cần thiết trong giai đoạn cài đặt thư viện nhưng không cần cho runtime.
2. Bộ nhớ đệm (cache) khi tải gói của pip và các file đối tượng trung gian sinh ra trong quá trình cài đặt dependencies. Multi-stage build dùng stage `runtime` trên nền `python:3.11-slim` chỉ copy thư mục `site-packages` và source code cần thiết, giúp loại bỏ toàn bộ các tệp dư thừa nói trên.

---

### Câu 4 — Thứ tự lệnh trong Dockerfile (CP2)

Sửa một ký tự trong `app/main.py` rồi build lại. Với Dockerfile của bạn, những
layer nào được dùng lại từ cache, layer nào phải chạy lại? Nếu bạn đặt
`COPY . .` lên trước `RUN pip install` thì kết quả khác thế nào?

- Khi sửa một ký tự trong `app/main.py`:
  - Các layer được dùng lại từ cache (CACHED): Tải base image `python:3.11-slim`, tạo user `appuser`, `COPY requirements.txt .`, `RUN pip install ...`, và copy `site-packages` từ builder sang runtime.
  - Layer phải chạy lại: Chỉ layer `COPY . .` và các lệnh sau nó phải thực thi lại vì checksum của context thư mục thay đổi khi sửa file code. Quá trình build hoàn thành gần như ngay lập tức (1-2 giây).
- Nếu đặt `COPY . .` lên trước `RUN pip install`:
  - Mỗi khi sửa một ký tự trong code, layer `COPY . .` bị vô hiệu hóa cache, kéo theo layer `RUN pip install` phía sau buộc phải chạy lại từ đầu. Docker sẽ phải tải lại toàn bộ các thư viện qua mạng, làm thời gian build kéo dài và lãng phí băng thông.

---

### Câu 5 — Vì sao không chạy bằng root (CP2)

Container mặc định chạy bằng root. Mô tả chuỗi sự kiện dẫn từ "một lỗ hổng
trong code Python của bạn" tới "kẻ tấn công có quyền cao trên máy host", và
lệnh `USER` cắt đứt chuỗi đó ở chỗ nào.

Chuỗi sự kiện:
1. Code ứng dụng tồn tại lỗ hổng (như Remote Code Execution qua lỗ hổng thư viện hoặc Command Injection), kẻ tấn công khai thác để thực thi shell tùy ý bên trong container.
2. Vì container chạy mặc định dưới quyền `root` (UID 0), kẻ tấn công sở hữu toàn bộ đặc quyền root trong môi trường container.
3. Kẻ tấn công kết hợp với các kỹ thuật container breakout (như khai thác lỗ hổng kernel của máy host, tận dụng Docker socket bị mount nhầm `/var/run/docker.sock`, hoặc container chạy mode privileged) để thoát ra ngoài không gian của máy host. Do tiến trình trong container ánh xạ trực tiếp UID 0 với root của máy host, kẻ tấn công chiếm luôn quyền điều khiển tối cao máy chủ thật.
4. **Lệnh `USER appuser` cắt đứt chuỗi sự kiện này**: Nó ép tiến trình chạy với user thường không có đặc quyền (UID 10001). Ngay cả khi chiếm được shell bên trong container, kẻ tấn công cũng không thể sửa đổi file hệ thống của container và không có quyền root để thực hiện các cuộc tấn công leo thang đặc quyền ra máy host.

---

### Câu 6 — Cửa sổ trượt (CP3)

Rate limit của bạn dùng sliding window 60 giây. Nếu thay bằng cách đếm theo
phút đồng hồ (reset lúc giây 00), một người dùng có thể gửi tối đa bao nhiêu
request trong 2 giây liên tiếp khi hạn mức là 10/phút? Giải thích cách đạt được
con số đó.

Người dùng có thể gửi tối đa **20 request** trong 2 giây liên tiếp.
Giải thích: Với cơ chế đếm theo phút đồng hồ (Fixed Window), hạn mức được reset về 0 vào đúng giây 00 của mỗi phút mới:
- Người dùng gửi 10 request vào giây cuối cùng của phút thứ nhất (giây `10:00:59`). Hệ thống ghi nhận 10/10 request cho phút đó (vẫn hợp lệ).
- Ngay tại giây tiếp theo (giây `10:01:00`), bộ đếm chuyển sang phút mới và được reset về 0. Người dùng gửi tiếp 10 request nữa.
Tổng cộng trong khoảng thời gian chỉ 2 giây (từ 10:00:59 đến 10:01:00), hệ thống đã phải xử lý tới 20 request, gấp đôi tải thiết kế cho phép. Sliding window ngăn chặn triệt để kẽ hở này bằng cách đo lường chính xác khoảng thời gian 60 giây trượt liên tục.

---

### Câu 7 — Rate limit và cost guard (CP3)

Hai cơ chế này khác nhau ở điểm nào? Cho một tình huống mà rate limit cho qua
nhưng cost guard phải chặn, và một tình huống ngược lại.

- **Điểm khác nhau**: Rate limit kiểm soát **tần suất/số lượng request** trong một đơn vị thời gian ngắn (ví dụ 10 request/phút) để bảo vệ hạ tầng máy chủ khỏi quá tải. Cost guard kiểm soát **tổng số tiền chi phí tài chính (USD)** tích lũy trong cả tháng dựa trên số token tiêu thụ thực tế của LLM để bảo vệ ngân sách.
- **Tình huống Rate limit cho qua nhưng Cost guard chặn**: Người dùng chỉ gửi 1 request duy nhất trong cả buổi sáng (tần suất hoàn toàn dưới 10 req/phút), nhưng tài khoản của người dùng này đã tiêu hết hạn mức $10.0 của tháng trước đó $\rightarrow$ Cost guard lập tức chặn và trả lỗi `402 Payment Required`.
- **Tình huống Cost guard cho qua nhưng Rate limit chặn**: Người dùng mới bắt đầu chu kỳ tháng, ngân sách còn nguyên $10.0, nhưng gửi dồn dập 15 request chỉ trong vòng 10 giây $\rightarrow$ Chi phí mới chỉ phát sinh vài cent (vẫn còn ngân sách), nhưng vượt quá ngưỡng 10 request/phút $\rightarrow$ Rate limiter chặn lại và trả lỗi `429 Too Many Requests`.

---

### Câu 8 — /health khác /ready (CP4)

Nếu gộp hai endpoint làm một và cho nó kiểm tra Redis, chuyện gì xảy ra với cụm
3 container khi Redis mất kết nối 30 giây? Trả lời theo đúng thứ tự sự kiện.

Thứ tự sự kiện xảy ra:
1. Redis gặp sự cố mạng hoặc khởi động lại, mất kết nối trong 30 giây.
2. Endpoint `/health` (đang gộp kiểm tra Redis) không kết nối được Redis nên trả về mã lỗi hoặc timeout.
3. Bộ điều phối (Orchestrator/Docker) coi `/health` là Liveness Probe $\rightarrow$ suy đoán rằng toàn bộ tiến trình ứng dụng của cả 3 container agent đều đã bị lỗi hoặc treo chết.
4. Orchestrator lập tức ra lệnh restart hoặc tiêu diệt cả 3 container agent cùng lúc.
5. Khi container mới khởi động lại, Redis vẫn chưa hồi phục $\rightarrow$ probe lại thất bại và container tiếp tục bị restart vòng lặp vô tận (CrashLoopBackOff).
6. Một sự cố gián đoạn tạm thời ở tầng dữ liệu biến thành thảm họa sập toàn bộ dịch vụ (cascading failure).
*(Khi tách đúng: `/health` độc lập giữ container sống; `/ready` trả 503 để Load Balancer tạm thời không điều phối traffic đến cho đến khi Redis kết nối lại bình thường).*

---

### Câu 9 — Stateless (CP4)

Chạy `docker compose up --scale agent=3` rồi gọi `/ask` nhiều lần với cùng một
`X-User-Id`. Quan sát `history_length` trong response. Nếu lịch sử được lưu
trong một dict Python thay vì Redis, bạn sẽ thấy con số đó thay đổi thế nào?

Nếu lưu trong dict Python ở RAM của process:
Các request liên tiếp của cùng một user sẽ được Load Balancer phân phối ngẫu nhiên hoặc xoay vòng (round-robin) đến 3 instance container agent khác nhau.
- Vì mỗi instance có một vùng nhớ RAM tách biệt, giá trị `history_length` trả về sẽ bị **nhảy loạn xạ và không tăng liên tục**. Ví dụ: request 1 vào agent 1 (`history_length = 0`), request 2 vào agent 2 (`history_length = 0`), request 3 vào agent 3 (`history_length = 0`), request 4 quay lại agent 1 (`history_length = 2`). Người dùng sẽ thấy agent bị "mất trí nhớ ngẫu nhiên".
- Ngược lại, khi lưu state tập trung vào Redis, bất kể request rơi vào container nào, container đó đều đọc và ghi chung vào Redis, giúp `history_length` tăng tuần tự và nhất quán (`0 -> 2 -> 4 -> 6...`).

---

### Câu 10 — Deploy thật (CP5)

Ghi lại **một** lỗi bạn gặp khi deploy lên cloud (build fail, health check
timeout, sai REDIS_URL, app không đọc `$PORT`...): thông báo lỗi là gì, bạn
tìm ra nguyên nhân bằng cách nào, và sửa ra sao?

- **Thông báo lỗi**: Khi kiểm tra kết nối với máy chủ Railway qua CLI và lệnh curl kiểm tra chứng chỉ HTTPS trên Windows, gặp lỗi timeout kết nối mạng `A connection attempt failed because the connected party did not properly respond after a period of time (os error 10060)` và `curl: (35) schannel: next InitializeSecurityContext failed: CRYPT_E_REVOCATION_OFFLINE (0x80092013)`.
- **Cách tìm ra nguyên nhân**: Chạy lệnh chẩn đoán mạng `Test-NetConnection -ComputerName backboard.railway.com -Port 443` cho kết quả `TcpTestSucceeded : False`, xác định dải IP của Railway đang bị nhà mạng tại Việt Nam chặn. Trong khi đó, kiểm tra `Test-NetConnection -ComputerName render.com -Port 443` cho kết quả `TcpTestSucceeded : True`. Lỗi của curl do tính năng kiểm tra thu hồi chứng chỉ (CRL revocation) của Windows SChannel bị timeout khi gặp mạng chập chờn.
- **Cách sửa**:
  1. Chuyển sang triển khai trên nền tảng Render thông qua file cấu hình `render.yaml` có sẵn trong repo, thiết lập Blueprint tự động tạo web service `day12-agent` kết nối tới `day12-redis`.
  2. Bổ sung cờ `--ssl-no-revoke` khi chạy curl trên Windows hoặc kiểm thử qua thư viện HTTP chuẩn `httpx`.
  3. Dịch vụ deploy trên Render hoạt động mượt mà, kết nối Redis thành công và vượt qua toàn bộ 9/9 bài test của Checkpoint 5.
