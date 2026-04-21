const express = require("express");
const http = require("http");
const { WebSocketServer } = require("ws");

const app = express();
const server = http.createServer(app);

app.get("/", (req, res) => {
  res.send("Embodied Interaction backend is running");
});

app.get("/healthz", (req, res) => {
  res.status(200).send("ok");
});

const wss = new WebSocketServer({ noServer: true });
const clients = new Set();

function safeSend(ws, data, isBinary = false) {
  if (ws.readyState === ws.OPEN) {
    ws.send(data, { binary: isBinary });
  }
}

function broadcast(sender, data, isBinary = false) {
  for (const client of clients) {
    if (client !== sender && client.readyState === client.OPEN) {
      client.send(data, { binary: isBinary });
    }
  }
}

wss.on("connection", (ws, req) => {
  clients.add(ws);

  const url = new URL(req.url, "http://localhost");
  const role = url.searchParams.get("role") || "unknown";

  console.log(`WS connected: role=${role}, clients=${clients.size}`);

  safeSend(
    ws,
    JSON.stringify({
      type: "connected",
      role,
      clients: clients.size,
      message: "WebSocket connection established"
    })
  );

  ws.on("message", (data, isBinary) => {
    if (isBinary) {
      broadcast(ws, data, true);
      return;
    }

    const text = data.toString();
    console.log(`WS message from ${role}:`, text.slice(0, 200));

    try {
      const json = JSON.parse(text);

      if (json.type === "ping") {
        safeSend(ws, JSON.stringify({ type: "pong", t: Date.now() }));
        return;
      }

      if (json.type === "bess" || json.type === "state" || json.type === "event") {
        broadcast(ws, JSON.stringify(json));
        return;
      }

      if (json.type === "frame" && typeof json.data === "string") {
        broadcast(ws, JSON.stringify(json));
        return;
      }

      broadcast(ws, text);
    } catch (err) {
      broadcast(ws, text);
    }
  });

  ws.on("close", () => {
    clients.delete(ws);
    console.log(`WS disconnected: role=${role}, clients=${clients.size}`);
  });

  ws.on("error", (err) => {
    console.error(`WS error from ${role}:`, err.message);
  });
});

server.on("upgrade", (req, socket, head) => {
  const url = new URL(req.url, "http://localhost");

  if (url.pathname !== "/ws") {
    socket.destroy();
    return;
  }

  wss.handleUpgrade(req, socket, head, (ws) => {
    wss.emit("connection", ws, req);
  });
});

const PORT = process.env.PORT || 10000;
server.listen(PORT, () => {
  console.log(`HTTP/WebSocket server listening on port ${PORT}`);
});