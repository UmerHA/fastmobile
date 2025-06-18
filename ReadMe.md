# FastMobile 🐍📱

> Server‑driven cross-platform mobile apps in **pure Python**

FastMobile lets you write your mobile app declaratively in Python. FastMobile converts your app to [HXML](https://hyperview.org/docs/guide_html), and [Hyperview](https://hyperview.org/) does the rest, turning your HXML into React Native.

FastMobile is based on [FastHTML](https://github.com/AnswerDotAI/fasthtml). In fact, it's only a slight adaptation of FastHTML to make it work with Hyperview, unlocking mobile.

## 1. Install
```bash
pip install fastmobile
```

This allows you to write your app. To view it, you’ll also need the Hyperview client. See [Getting Started](GettingStarted.md) guide for a step-by-step walkthrough.

## 2. Minimal Example
```python
from fastmobile import *

app, rt = fast_app()

@rt('/')
def get():
    return Screen(
        Body(
            Text('Hello, FastMobile!')
        )
    )

serve(port=8085)
```

## 3. Why FastMobile?

As [Hyperview docs](https://hyperview.org/docs/guide_introduction) notes, developing for mobile is slow and painful compared to the web. To quote them:

> On mobile:
>- we released code once a week,
>- it took 2 weeks for 80% of our users to get the update,
>- developer productivity was slowed down by the need to work across backend and frontend codebases.
>
>On the web:
>- we could release updates to our app many times a day,
>- all of our users always saw our updates immediately,
>- developers could build new features quickly by working in a single codebase.

Hyperview solves this allowing you to write server-first mobile apps. FastMobile makes this more convenient, because you can write Python and don't have to manually construct HXML.

## 4. FAQ

### Why not pure React Native?
You still get native feel, but your UI ships at web speed – no app‑store delays.

### How big is the binary?
The Hyperview shell is a thin RN wrapper; your Python code stays on the server.

### Can I mix FastHTML & FastMobile?
Partly. While you can't use FastHTML components because as Hyperview only supports a restricted set of tags, you can use the other mechanisms FastHTML has like `sessions`, `databases`, `beforeware` etc.

## 5. Further reading
- Hyperview docs ([hyperview.org](https://hyperview.org/))
- Hyperview reference ([hyperview.org/docs/reference_index](https://hyperview.org/docs/reference_index))
- FastHTML docs & blog posts ([github.com](https://github.com/AnswerDotAI/fasthtml), [answer.ai](https://www.answer.ai/posts/2024-08-03-fasthtml.html))
- Hypermedia Systems book – chapters 4‑7 for mobile hypermedia ([hypermedia.systems](https://hypermedia.systems/hyperview-a-mobile-hypermedia/))
