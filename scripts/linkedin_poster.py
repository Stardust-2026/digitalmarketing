#!/usr/bin/env python3
"""Auto-post to LinkedIn via Chrome DevTools Protocol."""
import json, urllib.request, sys, io, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

POST_TEXT = sys.argv[1] if len(sys.argv) > 1 else ""

if not POST_TEXT:
    # Read the latest content file
    import glob, os
    content_dir = "/home/josh/Development/Projects/digitalmarketing/content"
    files = sorted(glob.glob(f"{content_dir}/*.md"))
    if not files:
        print("No content files found")
        sys.exit(1)
    with open(files[-1]) as f:
        content = f.read()
    # Extract LinkedIn section
    if "===LINKEDIN===" in content:
        parts = content.split("===LINKEDIN===")[1].split("===YOUTUBE===")[0]
        POST_TEXT = parts.strip()
    else:
        POST_TEXT = content

# Connect to Chrome
tabs = json.loads(urllib.request.urlopen("http://localhost:9222/json", timeout=5).read())
ws_url = None
for t in tabs:
    u = t.get("url","")
    if "linkedin.com" in u:
        ws_url = t["webSocketDebuggerUrl"]
        break

if not ws_url:
    print("No LinkedIn tab found")
    sys.exit(1)

import websocket
ws = websocket.create_connection(ws_url, timeout=10)

def cdp(method, params=None):
    if params is None: params = {}
    cmd = json.dumps({"id":1,"method":method,"params":params})
    ws.send(cmd)
    return json.loads(ws.recv())

def eval_js(js):
    r = cdp("Runtime.evaluate", {"expression":js,"returnByValue":True,"awaitPromise":True})
    return r.get("result",{}).get("result",{}).get("value","")

def click_element(selector_fn):
    """Click an element by evaluating a JS function that returns {x, y} or null."""
    result = eval_js(f"""
    (function(){{
        {selector_fn}
        var r = findTarget();
        if (!r) return 'null';
        var rect = r.getBoundingClientRect();
        return JSON.stringify({{x: rect.x + rect.width/2, y: rect.y + rect.height/2}});
    }})();
    """)
    if result == 'null':
        return False
    coords = json.loads(result)
    cdp("Input.dispatchMouseEvent", {"type":"mousePressed","x":coords["x"],"y":coords["y"],"button":"left","clickCount":1})
    cdp("Input.dispatchMouseEvent", {"type":"mouseReleased","x":coords["x"],"y":coords["y"],"button":"left","clickCount":1})
    return True

# Step 1: Navigate to feed
cdp("Page.navigate", {"url":"https://www.linkedin.com/feed/"})
time.sleep(5)

# Step 2: Click "Start a post"
clicked = click_element("""
function findTarget() {
    var btns = document.querySelectorAll('button, div[role=button]');
    for (var b of btns) {
        var t = (b.innerText || '').toLowerCase().trim();
        var aria = (b.getAttribute('aria-label') || '').toLowerCase();
        if (t === 'start a post' || aria === 'start a post') return b;
    }
    return null;
}
""")
time.sleep(3)

# Step 3: Type the post
editor_found = eval_js("""
(function(){
    var ed = document.querySelector('[role=textbox][contenteditable=true]');
    if (ed) { ed.focus(); return 'found'; }
    return 'not found';
})();
""")

if editor_found == 'found':
    cdp("Input.insertText", {"text": POST_TEXT})
    time.sleep(2)
    
    # Step 4: Click Post
    clicked_post = click_element("""
    function findTarget() {
        var btns = document.querySelectorAll('button');
        for (var b of btns) {
            if (b.innerText.trim().toLowerCase() === 'post' && b.offsetParent !== null) return b;
        }
        return null;
    }
    """)
    
    if clicked_post:
        print("✅ Posted successfully!")
    else:
        print("⚠️ Text entered but Post button not found")
else:
    print("⚠️ Editor not found")

ws.close()
