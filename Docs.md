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
