# FastMobile 🐍📱

> Server‑driven cross-platform mobile apps in **pure Python**

FastMobile lets you write your mobile app declaratively in Python. FastMobile converts your app to [HXML](https://hyperview.org/docs/guide_html), and [Hyperview](https://hyperview.org/) does the rest, turning your HXML into React Native.

FastMobile is based on [FastHTML](https://github.com/AnswerDotAI/fasthtml). In fact, it's only a slight adaptation of FastHTML to make it work with Hyperview, unlocking mobile as well.

---

## 1. Why FastMobile?

* **Write once, run everywhere.** Describe your UI in Python; Hyperview renders it on iOS & Android.
* **Keep business logic on the server.** Push fixes instantly, ship without App‑Store waits.
* **Tiny learning curve.** If you know HTML or React Native’s Flexbox, you’re good.



---

## 2. How it works (in 60 seconds)

```
Python ──► FastMobile  ──► HXML  ──► Hyperview shell
          (Starlette)          (React‑Native)
```

1. Your Python endpoint returns **Hyperview XML (HXML)**.
2. The Hyperview client fetches that XML over HTTP, then lays out native views.([hyperview.org](https://hyperview.org/docs/guide_introduction?utm_source=chatgpt.com))

---

## 3. Install

```bash
pip install fastmobile   # requires Python ≥ 3.10
```

You’ll also need a Hyperview shell:

* **Expo Snack**: `expo install @instawork/hyperview`
* Or clone `github.com/Instawork/hyperview`

Connect the shell to `http://<server>:8085`.

---

## 4. Hello World

```python
# hello.py
from fastmobile import *

app, rt = fast_app()          # returns Starlette app + router helper

@rt('/')                      # map GET /
def home():
    return Screen(
        Body(
            Text('Hello, FastMobile!')
        )
    )

serve(port=8085)
```

Run `python hello.py`, then open your Hyperview app and navigate to `/`.
That’s it – a live native screen in under 20 lines.

---

## 5. Anatomy of a FastMobile app

| Piece          | What it does                                                                          |
| -------------- | ------------------------------------------------------------------------------------- |
| `fast_app()`   | Spins up a SQLite‑backed Starlette app and returns `(app, route_helper)`              |
| **Components** | `Doc`, `Screen`, `View`, `Text`, `Img`, `List`, … all map 1‑to‑1 to HXML tags         |
| **Styling**    | `Styles` + `Style` let you bundle CSS‑like rules; Flexbox is the default layout model |
| **Navigation** | `StackNav`, `TabNav`, `Navigator`, and `NavRoute` build native‑feeling navigation     |
| **Behavior**   | `Back`, `Dispatch`, and `On` express tap/submit gestures with zero JS                 |
| **Helpers**    | `margin()`, `padding()`, and `WhenFocused/Selected/Pressed` cut down on boilerplate   |

### 5.1 Styling shorthand

```python
Style('btn',
      padding='8 12',
      backgroundColor='blue',
)(WhenPressed(opacity=0.7))
```

* `padding='8 12'` expands to `paddingTop=8`, `paddingRight=12`, …

### 5.2 Dynamic content

```python
def tweet_list():
    return View(scroll=True)(*map(Tweet.__ft__, tweets))
```

Because `FT` nodes are just Python objects, you can map/filter/generate them with normal code.

---

## 6. Routing in depth

`rt(path)` is sugar for `@app.route(path, methods=['GET'])`.
Under the hood FastMobile:

1. Detects whether the request is full doc or fragment.
2. Wraps fragments in `<screen>` automatically so the client never breaks.
3. Adds caching & background tasks where needed.

---

## 7. Production tips

* **CORS** – add `--cors` or mount a Starlette `CORSMiddleware`.
* **HTTPS** – put a reverse proxy (Caddy, Nginx) in front, or deploy to Railway/Vercel.
* **Hot‑reload** – `serve(reload=True)` reloads on file‑save.

---

## 8. Example apps

* \`\` – Twitter‑style feed with avatars & flex layout.
* \`\` – Bottom‑tab navigator with per‑tab screens.

Clone the repo and run:

```bash
python sassy.py  # port 8085
```

then open `hyperview://localhost:8085/`.

---

## 9. FAQ

### Why not pure React Native?

You still get native feel, but your UI ships at web speed – no app‑store delays.

### How big is the binary?

The Hyperview shell is a thin RN wrapper; your Python code stays on the server.

### Can I mix FastHTML & FastMobile?

Yes – both share the same `FT` core, so you can reuse components and styles across web and mobile.

---

## 10. Further reading

* Hyperview docs & HXML spec ([hyperview.org](https://hyperview.org/?utm_source=chatgpt.com))
* FastHTML docs & blog posts ([github.com](https://github.com/AnswerDotAI/fasthtml?utm_source=chatgpt.com), [answer.ai](https://www.answer.ai/posts/2024-08-03-fasthtml.html?utm_source=chatgpt.com))
* Hypermedia Systems book – chapters 4‑7 for mobile hypermedia ([hypermedia.systems](https://hypermedia.systems/hyperview-a-mobile-hypermedia/?utm_source=chatgpt.com), [hypermedia.systems](https://hypermedia.systems/building-a-contacts-app-with-hyperview/?utm_source=chatgpt.com))

---

# Get Started Guide 🚀

### Step 1 – Install FastMobile

```bash
python -m venv .venv
source .venv/bin/activate
pip install fastmobile
```

### Step 2 – Create `app.py`

```python
from fastmobile import *

app, rt = fast_app()

@rt('/')
def home():
    return Screen(Body(Text('👋 Hello from FastMobile')))

serve(port=8085)
```

### Step 3 – Open the Hyperview shell

Point the shell to `http://127.0.0.1:8085/`.

> Tip: On a physical device use your computer’s LAN IP, e.g. `http://192.168.1.5:8085/`.

### Step 4 – Edit & reload

Change the text and hit *Save* – the shell automatically fetches the new XML. No rebuilds.

### Step 5 – Add styles

```python
style = Styles(
    Style('title', fontSize=24, fontWeight='bold', margin='t24 b12'),
)

@rt('/')
def home():
    return Screen(
        style,
        Body(View(Text('Welcome', style='title')))
    )
```

### Step 6 – Deploy

```bash
pip install uvicorn
uvicorn app:app --port 80 --host 0.0.0.0
```

Then push to any VPS or container platform.

---

Happy building! 🎉
