import http from "node:http";
import { readFile } from "node:fs/promises";
import { extname, join, normalize } from "node:path";

const root = process.cwd();
const port = Number(process.env.PORT || 5173);
const mime = {
  ".html": "text/html; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".json": "application/json; charset=utf-8",
  ".svg": "image/svg+xml"
};

http.createServer(async (request, response) => {
  const url = new URL(request.url, `http://localhost:${port}`);
  const pathname = decodeURIComponent(url.pathname);
  const target = pathname === "/" || !extname(pathname) ? "/index.html" : pathname;
  const filePath = normalize(join(root, target));

  if (!filePath.startsWith(root)) {
    response.writeHead(403);
    response.end("Forbidden");
    return;
  }

  try {
    const content = await readFile(filePath);
    response.writeHead(200, { "Content-Type": mime[extname(filePath)] || "application/octet-stream" });
    response.end(content);
  } catch {
    const content = await readFile(join(root, "index.html"));
    response.writeHead(200, { "Content-Type": mime[".html"] });
    response.end(content);
  }
}).listen(port, () => {
  console.log(`Vue fallback server: http://localhost:${port}`);
});
