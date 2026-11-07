# networkinstructions

Web chat page for the Network Instructors CCNA / networking assistant, an n8n AI Agent workflow.

## Files

| File | What it is |
|---|---|
| `index.html` | The chat page. One self-contained HTML file, no build step. |
| `deploy_page.py` | Creates or updates the n8n workflow that serves the page, then publishes it. |

## How it works

The page sends each message to the n8n Chat Trigger webhook as JSON:

```json
{"action": "sendMessage", "sessionId": "<random id per chat>", "chatInput": "<question>"}
```

n8n replies with `{"output": "<answer>"}`. The `sessionId` lets the agent's memory keep the conversation together; **New chat** starts a new one.

## Run it

- Locally: open `index.html` in a browser.
- Hosted in n8n: `python3 deploy_page.py` (macOS; reads the n8n API key from Keychain, service `n8n-api-key`). The page is then served at `http://<n8n-host>:5678/webhook/networkinstructors`.

The webhook URL is set in `DEFAULT_URL` at the top of the page's script and can be changed under **Settings**.

www.networkinstructors.com
