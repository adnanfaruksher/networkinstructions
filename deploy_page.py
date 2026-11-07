#!/usr/bin/env python3
"""Create (or update) the n8n workflow that serves Networkinstructors-Assistant.html
at http://100.111.83.35:5678/webhook/networkinstructors, then publish it.
API key read from macOS Keychain (service n8n-api-key)."""
import json, subprocess, sys, uuid, urllib.request, pathlib

API = "http://100.111.83.35:5678/api/v1"
NAME = "Networkinstructors UI page"
PATH = "networkinstructors"
html = (pathlib.Path(__file__).parent / "index.html").read_text()
assert "{{" not in html and not html.startswith("="), "page would be read as an n8n expression"
key = subprocess.check_output(["security", "find-generic-password", "-s", "n8n-api-key", "-w"], text=True).strip()

def call(method, url, body=None):
    req = urllib.request.Request(API + url, method=method,
        data=None if body is None else json.dumps(body).encode(),
        headers={"X-N8N-API-KEY": key, "Content-Type": "application/json", "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read() or b"{}")

wf = {
  "name": NAME,
  "nodes": [
    {"id": str(uuid.uuid4()), "name": "Page request", "type": "n8n-nodes-base.webhook", "typeVersion": 2,
     "position": [0, 0], "webhookId": str(uuid.uuid5(uuid.NAMESPACE_URL, PATH)),
     "parameters": {"httpMethod": "GET", "path": PATH, "responseMode": "responseNode", "options": {}}},
    {"id": str(uuid.uuid4()), "name": "Send page", "type": "n8n-nodes-base.respondToWebhook", "typeVersion": 1.1,
     "position": [240, 0],
     "parameters": {"respondWith": "text", "responseBody": html,
                    "options": {"responseHeaders": {"entries": [
                        {"name": "Content-Type", "value": "text/html; charset=utf-8"},
                        {"name": "Cache-Control", "value": "no-cache"}]}}}}],
  "connections": {"Page request": {"main": [[{"node": "Send page", "type": "main", "index": 0}]]}},
  "settings": {"executionOrder": "v1", "saveDataSuccessExecution": "none"},
}

existing = [w for w in call("GET", "/workflows?limit=250")["data"] if w["name"] == NAME]
if existing:
    wid = existing[0]["id"]
    call("PUT", f"/workflows/{wid}", wf)
    print("updated", wid)
else:
    wid = call("POST", "/workflows", wf)["id"]
    print("created", wid)
r = call("POST", f"/workflows/{wid}/activate")
print("active:", r.get("active"))
print(f"URL: http://100.111.83.35:5678/webhook/{PATH}")
