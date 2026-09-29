HTML_PAGE = """<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Day 12 Production AI Agent — UI</title>
  <style>
    :root {
      --bg: #0f172a;
      --card-bg: #1e293b;
      --border: #334155;
      --primary: #3b82f6;
      --primary-hover: #2563eb;
      --text: #f8fafc;
      --text-muted: #94a3b8;
      --success: #22c55e;
      --danger: #ef4444;
      --warning: #f59e0b;
      --bubble-user: #1d4ed8;
      --bubble-bot: #1e293b;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }
    body { background: var(--bg); color: var(--text); height: 100vh; display: flex; flex-direction: column; overflow: hidden; }
    
    /* Header */
    header { background: #0b1120; border-bottom: 1px solid var(--border); padding: 12px 24px; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 12px; }
    .brand { display: flex; align-items: center; gap: 10px; }
    .brand h1 { font-size: 1.15rem; font-weight: 700; color: #fff; display: flex; align-items: center; gap: 8px; }
    .brand span { font-size: 0.8rem; background: #2563eb33; color: #60a5fa; border: 1px solid #3b82f655; border-radius: 6px; padding: 2px 8px; }
    .status-group { display: flex; align-items: center; gap: 10px; font-size: 0.8rem; }
    .badge { display: inline-flex; align-items: center; gap: 6px; padding: 4px 10px; border-radius: 9999px; font-weight: 500; border: 1px solid transparent; }
    .badge-ok { background: #14532d44; color: #4ade80; border-color: #22c55e44; }
    .badge-err { background: #7f1d1d44; color: #f87171; border-color: #ef444444; }
    .dot { width: 8px; height: 8px; border-radius: 50%; background: currentColor; }
    .dot.pulse { animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite; }
    @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.3; } }

    /* Settings Banner */
    .config-bar { background: #131d31; border-bottom: 1px solid var(--border); padding: 8px 24px; display: flex; align-items: center; gap: 16px; font-size: 0.85rem; flex-wrap: wrap; }
    .config-item { display: flex; align-items: center; gap: 8px; }
    .config-item label { color: var(--text-muted); font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.05em; font-weight: 600; }
    .config-input { background: #0b1120; border: 1px solid var(--border); color: #fff; padding: 5px 10px; border-radius: 6px; font-size: 0.85rem; outline: none; }
    .config-input:focus { border-color: var(--primary); }
    .api-key-input { width: 260px; font-family: monospace; }
    .user-id-input { width: 100px; }

    /* Main Container */
    main { flex: 1; display: flex; flex-direction: column; overflow: hidden; max-width: 960px; width: 100%; margin: 0 auto; padding: 16px 20px; }

    /* Chat Messages Box */
    #chat-box { flex: 1; overflow-y: auto; display: flex; flex-direction: column; gap: 14px; padding-right: 6px; }
    #chat-box::-webkit-scrollbar { width: 6px; }
    #chat-box::-webkit-scrollbar-thumb { background: var(--border); border-radius: 4px; }

    .msg { display: flex; flex-direction: column; max-width: 82%; animation: fadeIn 0.25s ease-out; }
    @keyframes fadeIn { from { opacity: 0; transform: translateY(6px); } to { opacity: 1; transform: translateY(0); } }
    .msg.user { align-self: flex-end; }
    .msg.bot { align-self: flex-start; }

    .bubble { padding: 12px 16px; border-radius: 12px; font-size: 0.95rem; line-height: 1.5; word-break: break-word; }
    .msg.user .bubble { background: var(--bubble-user); color: #fff; border-bottom-right-radius: 2px; }
    .msg.bot .bubble { background: var(--bubble-bot); color: var(--text); border: 1px solid var(--border); border-bottom-left-radius: 2px; }

    .meta { display: flex; flex-wrap: wrap; gap: 8px; font-size: 0.75rem; color: var(--text-muted); margin-top: 4px; padding: 0 4px; }
    .meta-tag { background: #0f172a; padding: 2px 6px; border-radius: 4px; border: 1px solid #33415566; }

    /* Chips */
    .chips { display: flex; flex-wrap: wrap; gap: 8px; margin: 12px 0; }
    .chip { background: #1e293b; border: 1px solid var(--border); color: #cbd5e1; font-size: 0.8rem; padding: 6px 12px; border-radius: 9999px; cursor: pointer; transition: all 0.15s; }
    .chip:hover { background: #334155; color: #fff; border-color: var(--primary); }

    /* Input Footer */
    .input-box { display: flex; gap: 10px; background: var(--card-bg); border: 1px solid var(--border); border-radius: 12px; padding: 8px 12px; margin-top: 12px; align-items: flex-end; }
    .input-box:focus-within { border-color: var(--primary); box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2); }
    textarea { flex: 1; background: transparent; border: none; outline: none; color: #fff; font-size: 0.95rem; resize: none; max-height: 120px; line-height: 1.4; padding: 4px 0; }
    button.send-btn { background: var(--primary); color: #fff; border: none; border-radius: 8px; padding: 8px 16px; font-weight: 600; cursor: pointer; transition: background 0.15s; display: flex; align-items: center; gap: 6px; }
    button.send-btn:hover { background: var(--primary-hover); }
    button.send-btn:disabled { opacity: 0.5; cursor: not-allowed; }

    .alert { padding: 10px 14px; border-radius: 8px; font-size: 0.85rem; margin-top: 6px; }
    .alert-danger { background: #450a0a; border: 1px solid #991b1b; color: #fca5a5; }
    .alert-warning { background: #451a03; border: 1px solid #b45309; color: #fcd34d; }

    /* Test Actions */
    .actions-bar { display: flex; justify-content: space-between; align-items: center; margin-top: 8px; font-size: 0.8rem; color: var(--text-muted); }
    .text-btn { background: none; border: none; color: #60a5fa; cursor: pointer; text-decoration: underline; font-size: 0.8rem; }
  </style>
</head>
<body>

  <header>
    <div class="brand">
      <h1>🤖 Day 12 Production Agent</h1>
      <span>Render Cloud</span>
    </div>
    <div class="status-group">
      <div id="badge-health" class="badge badge-ok">
        <span class="dot pulse"></span>
        <span id="txt-health">Liveness: OK</span>
      </div>
      <div id="badge-ready" class="badge badge-ok">
        <span class="dot pulse"></span>
        <span id="txt-ready">Redis: Ready</span>
      </div>
    </div>
  </header>

  <div class="config-bar">
    <div class="config-item">
      <label for="apiKey">X-API-Key</label>
      <input id="apiKey" class="config-input api-key-input" type="password" placeholder="Nhập AGENT_API_KEY..." />
      <button class="text-btn" onclick="toggleKeyVisibility()">Hiện/Ẩn</button>
    </div>
    <div class="config-item">
      <label for="userId">X-User-Id</label>
      <input id="userId" class="config-input user-id-input" type="text" value="sv01" />
    </div>
    <button class="text-btn" onclick="saveConfig()">Lưu cấu hình</button>
  </div>

  <main>
    <div id="chat-box">
      <!-- Welcome Message -->
      <div class="msg bot">
        <div class="bubble">
          👋 Chào bạn! Mình là AI Agent được triển khai trên <strong>Render Cloud</strong> với hạ tầng chuẩn Production:
          <ul style="margin: 8px 0 8px 20px; font-size: 0.9rem;">
            <li>🛡️ <strong>Authentication</strong> qua <code>X-API-Key</code> (constant-time digest)</li>
            <li>⏱️ <strong>Rate Limiter</strong> cửa sổ trượt (Sliding Window ZSET trên Redis)</li>
            <li>💰 <strong>Cost Guard</strong> kiểm soát chi phí token theo từng tháng</li>
            <li>🔄 <strong>Conversation Store</strong> phân tán trên Redis (Stateless)</li>
          </ul>
          Hãy nhập câu hỏi bên dưới hoặc bấm gợi ý để thử nghiệm nhé!
        </div>
      </div>
    </div>

    <!-- Suggested chips -->
    <div class="chips">
      <div class="chip" onclick="askPreset('Docker multi-stage build mang lại lợi ích gì?')">🐳 Docker multi-stage là gì?</div>
      <div class="chip" onclick="askPreset('Tại sao cần phân biệt liveness probe và readiness probe?')">🩺 Liveness vs Readiness?</div>
      <div class="chip" onclick="askPreset('Sliding window rate limiter bằng Redis ZSET hoạt động thế nào?')">⏱️ Redis Sliding Window?</div>
      <div class="chip" onclick="testSpam()">⚡ Test spam 12 requests (Kiểm tra Rate limit 429)</div>
    </div>

    <div class="input-box">
      <textarea id="questionInput" rows="1" placeholder="Nhập câu hỏi cho AI Agent... (Enter để gửi)"></textarea>
      <button id="sendBtn" class="send-btn" onclick="sendQuestion()">
        <span>Gửi</span>
      </button>
    </div>

    <div class="actions-bar">
      <span>Đọc tài liệu API: <a href="/docs" target="_blank" style="color: #60a5fa;">/docs (Swagger UI)</a></span>
      <button class="text-btn" onclick="clearChat()">Xóa màn hình</button>
    </div>
  </main>

  <script>
    const chatBox = document.getElementById("chat-box");
    const input = document.getElementById("questionInput");
    const sendBtn = document.getElementById("sendBtn");
    const apiKeyInput = document.getElementById("apiKey");
    const userIdInput = document.getElementById("userId");

    // Load saved settings
    apiKeyInput.value = localStorage.getItem("agent_api_key") || "aLJ3UtUoYESCMcIDTJnPSpKy3HXP42ldVoOcFkr3kjo";
    userIdInput.value = localStorage.getItem("agent_user_id") || "sv01";

    function saveConfig() {
      localStorage.setItem("agent_api_key", apiKeyInput.value.trim());
      localStorage.setItem("agent_user_id", userIdInput.value.trim());
      alert("Đã lưu API Key và User ID vào trình duyệt!");
    }

    function toggleKeyVisibility() {
      apiKeyInput.type = apiKeyInput.type === "password" ? "text" : "password";
    }

    // Auto resize textarea
    input.addEventListener("input", function() {
      this.style.height = "auto";
      this.style.height = Math.min(this.scrollHeight, 120) + "px";
    });

    input.addEventListener("keydown", function(e) {
      if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        sendQuestion();
      }
    });

    function askPreset(txt) {
      input.value = txt;
      sendQuestion();
    }

    function clearChat() {
      chatBox.innerHTML = "";
    }

    function appendMessage(role, text, meta) {
      const msgDiv = document.createElement("div");
      msgDiv.className = `msg ${role}`;

      const bubble = document.createElement("div");
      bubble.className = "bubble";
      bubble.innerText = text;
      msgDiv.appendChild(bubble);

      if (meta) {
        const metaDiv = document.createElement("div");
        metaDiv.className = "meta";
        metaDiv.innerHTML = `
          <span class="meta-tag">⚡ ${meta.latency}ms</span>
          <span class="meta-tag">🪙 In: ${meta.tokens_in || 0} / Out: ${meta.tokens_out || 0}</span>
          <span class="meta-tag">💵 Lượt này: $${Number(meta.cost_usd || 0).toFixed(5)}</span>
          <span class="meta-tag">📈 Tháng này: $${Number(meta.spent_this_month_usd || 0).toFixed(5)}</span>
          <span class="meta-tag">📚 Lịch sử: ${meta.history_length || 0} turn</span>
        `;
        msgDiv.appendChild(metaDiv);
      }

      chatBox.appendChild(msgDiv);
      chatBox.scrollTop = chatBox.scrollHeight;
    }

    function appendAlert(type, text) {
      const msgDiv = document.createElement("div");
      msgDiv.className = "msg bot";
      const alertDiv = document.createElement("div");
      alertDiv.className = `alert alert-${type}`;
      alertDiv.innerHTML = text;
      msgDiv.appendChild(alertDiv);
      chatBox.appendChild(msgDiv);
      chatBox.scrollTop = chatBox.scrollHeight;
    }

    async function sendQuestion() {
      const question = input.value.trim();
      if (!question) return;

      const apiKey = apiKeyInput.value.trim();
      const userId = userIdInput.value.trim() || "anonymous";

      appendMessage("user", question);
      input.value = "";
      input.style.height = "auto";
      sendBtn.disabled = true;

      const start = performance.now();
      try {
        const res = await fetch("/ask", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-API-Key": apiKey,
            "X-User-Id": userId
          },
          body: JSON.stringify({ question: question })
        });

        const latency = Math.round(performance.now() - start);

        if (res.status === 200) {
          const data = await res.json();
          appendMessage("bot", data.answer, { ...data, latency });
        } else if (res.status === 401) {
          appendAlert("danger", "🔒 <strong>401 Unauthorized</strong>: API Key không hợp lệ hoặc bị thiếu. Hãy điền đúng <code>AGENT_API_KEY</code> ở thanh cấu hình phía trên.");
        } else if (res.status === 429) {
          const retryAfter = res.headers.get("Retry-After") || 60;
          appendAlert("warning", `⏱️ <strong>429 Too Many Requests</strong>: Bạn đã gọi quá giới hạn trong phút. Vui lòng thử lại sau <strong>${retryAfter}s</strong>.`);
        } else if (res.status === 402) {
          appendAlert("danger", "💰 <strong>402 Payment Required</strong>: Bạn đã vượt ngân sách chi phí AI trong tháng.");
        } else {
          const err = await res.text();
          appendAlert("danger", `❌ Lỗi (${res.status}): ${err}`);
        }
      } catch (err) {
        appendAlert("danger", `🔌 Lỗi kết nối: ${err.message}`);
      } finally {
        sendBtn.disabled = false;
      }
    }

    // Ping health & ready
    async function checkProbes() {
      try {
        const hRes = await fetch("/health");
        const hData = await hRes.json();
        const bHealth = document.getElementById("badge-health");
        const tHealth = document.getElementById("txt-health");
        if (hRes.status === 200 && hData.status === "ok") {
          bHealth.className = "badge badge-ok";
          tHealth.innerText = "Liveness: OK";
        } else {
          bHealth.className = "badge badge-err";
          tHealth.innerText = "Liveness: DOWN";
        }
      } catch (e) {
        document.getElementById("badge-health").className = "badge badge-err";
        document.getElementById("txt-health").innerText = "Liveness: ERR";
      }

      try {
        const rRes = await fetch("/ready");
        const rData = await rRes.json();
        const bReady = document.getElementById("badge-ready");
        const tReady = document.getElementById("txt-ready");
        if (rRes.status === 200 && rData.redis === true) {
          bReady.className = "badge badge-ok";
          tReady.innerText = "Redis: Ready";
        } else {
          bReady.className = "badge badge-err";
          tReady.innerText = "Redis: Disconnected";
        }
      } catch (e) {
        document.getElementById("badge-ready").className = "badge badge-err";
        document.getElementById("txt-ready").innerText = "Redis: ERR";
      }
    }

    // Test Rate Limiter by sending 12 requests in a row
    async function testSpam() {
      appendAlert("warning", "🚀 Đang gửi nhanh 12 requests liên tiếp để thử nghiệm Redis Sliding Window Rate Limiter...");
      for (let i = 1; i <= 12; i++) {
        input.value = `Spam test câu số ${i}`;
        await sendQuestion();
        await new Promise(r => setTimeout(r, 100));
      }
    }

    checkProbes();
    setInterval(checkProbes, 15000);
  </script>
</body>
</html>
"""
