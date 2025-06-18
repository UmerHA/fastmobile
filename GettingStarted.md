# Getting Started Guide

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
