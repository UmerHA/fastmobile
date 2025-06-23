# Getting Started Guide

It might seem a bit daunting to get started with FastMobile, but it's actually quite simple. You need 3 things:

1. Server: A `fastmobile` server you write in Python.
2. Client: The Hyperview client to turn your server's output into a React Native mobile app.
3. Viewer: A way to run mobile apps on your computer or phone. We recommend Expo.

Let's get started!


## Step 1 – Create a FastMobile server

First, create a new directory for your app.

```bash
mkdir app
cd app
```

Then, install the `fastmobile` package.
```bash
pip install fastmobile
```

Now create a `app.py` file with the following content. This is your FastMobile server.

```python
from fastmobile import *

app, rt = fast_app()

@rt('/')
def home():
    return Screen(Body(Text('👋 Hello from FastMobile')))

serve(port=8085)
```

Note the port `8085`. We'll use this later.

Finally, start the server.
```bash
python app.py
```

You can verify the server is running by visiting `http://127.0.0.1:8085/` in your browser.

## Step 2 - Install and start the viewer

We recommend using Expo Orbit. Visit https://expo.dev/orbit to download and install it.

Once installed, use the UI to start an emulator.
The Hyperview client which we start below will run as an app on the emulator.

## Step 3 - Setup the Hyperview client

Clone the Hyperview client repo.

```bash
cd .. # back to parent directory
git clone https://github.com/UmerHA/hyperview-client
cd hyperview-client
```

This repo is a stripped down version of the original Hyperview repo, containing just the client part.

Not that in `App.tsx`, the entry point is ```entrypointUrl={`${Constants.expoConfig?.extra?.baseUrl}/`}```.
Therefore the start page of your app points to your server's `/` route.

Running the client is slighty different depending on your platform:

### 🤖 Android Emulator
First, you need to tell the emulator how to map ports from your computer to the emulator.
To keep it simple, we'll use the same port on both sides.
Our port is `8085`, so you can

```bash
adb reverse tcp:8085 tcp:8085
```

Then, run the client.

```bash
yarn android
```

### 🍏 iOS Emulator
No need to map ports, just run the client.

```bash
yarn ios
```

### 📱 Physical Device
```bash
BASE_URL="http://$(ifconfig en0 | grep inet | grep -v inet6 | awk '{print $2}'):8085"
yarn start
```
