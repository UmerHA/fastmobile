from fastmobile import *
from pathlib import Path
from dataclasses import dataclass, field
from collections import defaultdict
from typing import List as L
import random

AV_DIR = Path("avatars")
PIC_DIR = Path("photos")
AV = list(AV_DIR.glob("*.jp*g"))+list(AV_DIR.glob("*.png"))
PIC = list(PIC_DIR.glob("*.jp*g"))+list(PIC_DIR.glob("*.png"))

@dataclass
class usr():
    uid: int
    name: str
    loc: str
    file: str
    posts: int = field(default_factory=lambda: random.randint(1000, 10000))
    follower: int = field(default_factory=lambda: random.randint(1000, 10000))
    following: int = field(default_factory=lambda: random.randint(1000, 10000))
    img_lst: L[Path] = field(default_factory=lambda: ["/"+str(p) for p in PIC])
    
loc_lst = ["Las Vegas, CA", "Alpha Centaury", "Right Behind Event Horizon", "Midgard", "Hilbert's Hotel", "Andromeda"]
usr_lst = [usr(i, f.stem, l, "/"+str(f)) for i,f,l in zip(range(len(AV)), AV, loc_lst)]

# Create a global dictionary to store likes
# Map image paths to their like counts
image_likes = defaultdict(int)
# Maps user ID to set of liked image paths
user_likes = defaultdict(set)
# Initialize with some random likes for existing images
for p in PIC: image_likes[str(p)] = random.randint(5, 100)

app, rt = fast_app()

sty = Styles({
    # --- generic ----------------------------------------------------
    "base": {"fontSize": 24},
    "pad":  {"paddingLeft": 24},

    # --- layout / containers ---------------------------------------
    "list-container":   {"flex": 1, "padding": "b280"},
    "scroll-container": {"flex": 1},

    # --- image ------------------------------------------------------
    "image":           {"height": 375, "width": 375, "flex": 1},
    "image-container": {"alignItems": "center", "width": "100%"},
    
    # --- stories row -----------------------------------------------
    "stories": {
        "backgroundColor": "#F4F4F4",
        "flex": 1,
        "flexDirection": "row",
        "paddingLeft": 8,
    },
    "story": {
        "alignItems": "center",
        "flex": 1,
        "margin": "t26 r8 b18 l8",
    },
    "story-avatar": {
        "backgroundColor": "#F4F4F4",
        "borderRadius": 32,
        "height": 64,
        "width": 64,
    },
    "story-username": {"fontSize": 14, "fontWeight": "bold", "marginTop": 4},

    # --- image header ----------------------------------------------
    "image-header": {
        "alignItems": "center",
        "backgroundColor": "white",
        "flex": 1,
        "flexDirection": "row",
        "justifyContent": "space-between",
        "padding": 16,
    },
    "image-header-avatar": {
        "backgroundColor": "#F4F4F4",
        "borderRadius": 34,
        "height": 50,
        "width": 50,
        "margin": "t10 b10 l5",
    },
    "image-header-left":         {"flexDirection": "row"},
    "image-header-left-labels":  {"justifyContent": "center", "marginLeft": 8},
    "image-header-username":     {"color": "#4E4D4D", "fontSize": 14, "fontWeight": "bold"},
    "image-header-location":     {"color": "#BDC4C4", "fontSize": 14, "fontWeight": "normal"},
    "image-header-right":        {"flexDirection": "row"},
    "image-header-more":         {"color": "#BDC4C4", "fontSize": 14, "fontWeight": "bold"},
    
    # --- navigation -------------------------------------------------
    "back":     {"flex": 1, "padding": 15, "width": 24, "height": 24},
    "back-btn": {"padding": 10, "margin": "t16 r4 b8 l2"},
   
    # --- overlay text ----------------------------------------------
    "center-txt": {
        "fontSize": 24,
        "fontWeight": "bold",
        "textAlign": "center",
        "alignItems": "center",
        "justifyContent": "center",
        "flex": 1,
        "position": "absolute",
        "top": 30,
        "left": 0,
        "right": 0,
        "bottom": 0,
    },


    # --- profile header --------------------------------------------
    "username": {"paddingBottom": 20, "marginBottom": 15},
    "line": {
        "backgroundColor": "#808080",
        "height": 2,
        "width": "90%",
        "marginLeft": "5%",
        "marginRight": "5%",
    },
    "profile-stats": {
        "flexDirection": "row",
        "justifyContent": "space-around",
        "padding": "t20 b20",
        "width": "80%",
    },
    "stat-column": {"alignItems": "center"},
    "stat-number": {"fontSize": 18, "fontWeight": "bold"},
    "stat-label":  {"fontSize": 14, "color": "#666666"},
    "profile-pic": {"width": 60, "height": 60, "borderRadius": 30, "margin": "t15 b15"},
    "profile-section": {
        "flexDirection": "row",
        "alignItems": "center",
        "padding": "l15 r15",
        "width": "100%",
    },

    # --- bio --------------------------------------------------------
    "bio-section": {"padding": "l20 r20", "margin": "t10 b20"},
    "bio-name":    {"fontSize": 14, "fontWeight": "bold", "marginBottom": 4},
    "bio-text":    {"fontSize": 14, "color": "#262626"},

    # --- image grid -------------------------------------------------
    "image-grid": {"flexDirection": "row", "flexWrap": "wrap", "width": "100%"},
    "grid-image": {"width": "33.33%", "aspectRatio": 1, "padding": 1},
    "grid-image-inner": {
        "width": "100%",
        "height": "100%",
        "backgroundColor": "#EFEFEF",
    },

    # --- post footer ------------------------------------------------
    "likes-count": {"fontSize": 14, "fontWeight": "bold", "marginTop": 8, "marginLeft": 16, "color": "#4E4D4D"},
    "actionbar":   {"flexDirection": "row", "justifyContent": "space-between", "margin": "t8 r16 l16"},
    "actionbar-left": {"flexDirection": "row"},
    "heart-icon":     {"width": 24, "height": 24, "marginRight": 8},
})

def head():
    return View(
            (View(
                (Img(source=u.file,  href=f"/up/{u.uid}", style="story-avatar"), 
                 Text(u.name, numberOfLines="1", href=f"/up/{u.uid}", style="story-username")), 
            style="story") for u in usr_lst),
            scroll="true", scroll_orientation="horizontal")

def card(u):
    return View(
        View(style="image-header-left")(
             Img(source=u.file, style="image-header-avatar"),
             View(
                Text(u.name, style="image-header-username"),
                Text(u.loc, style="image-header-location"),
                style="image-header-left-labels"
             ),
        )
    )

def lst_vw():
    return View(style="list-container")(
        View((
            View(
                View(
                    card(u),
                    Img(source=str(p), style="image image-container"),
                    View(
                        View(
                            Img(
                                source="/icons/heart2.png",
                                style="heart-icon",
                                # special chars (., /) don't work in href
                                href=f"/like/{i}",
                                action="replace",
                                target=f"likes-{i}"
                            ),
                            Text(f"{image_likes[str(p)]} likes", id=f"likes-{i}", style="likes-count"),
                            style="actionbar-left"
                        ),
                        style="actionbar"
                    )
                ), key=str(p)
            ) for i, (u, p) in enumerate(zip(usr_lst, reversed(PIC[:6])))), 
        )
    )

@rt('/')
def get():
    return Doc(StackNav(NavRoute(href="/home", id="home")))

@rt('/home')
def get():
    return sty, Body(View(head(), View(lst_vw(), scroll="true")))


def stat(val, label):
    return View(style="stat-column")(
        Text(f"{val}", style="stat-number"),
        Text(label, style="stat-label"))

@rt('/up/{uid}')
def get(uid: int):
    u = usr_lst[uid]
    return sty, Body(
        View(
            View(Text(u.name, style="center-txt"), View(Img(source="icons/back.svg", style="back"), href="/home", action="back", style="back-btn"), style="username"),
            View(style="line"),
            View(style="profile-section")(
                Img(source=u.file, style="profile-pic"),
                View(
                    stat(u.posts, "posts"),
                    stat(u.follower, "followers"),
                    stat(u.following, "following"))
            ), 
            View(style="bio-section")(
                Text(u.name.upper(), style="bio-name"),
                Text("I'm a synthetic life form with artificial intelligence.\nLove long walks on the beach and pumpkin spice everything!",
                     style="bio-text")                
            ),
            View(style="image-grid")(
                View(style="grid-image")(
                    Img(source=img, style="grid-image-inner"),
                ) for img in u.img_lst[:]
            )
    ))
    
# route handler to handle likes
@rt('/like/test')
def get():
    image_path=PIC[-1]
    image_likes[image_path] += 1
    return Text(f"{image_likes[image_path]} likes", id=f"likes-{image_path}", style="likes-count")

# route handler to handle likes
@rt('/like/{image_id}')
def get(image_id: int):
    image_path = str(PIC[int(image_id)])
    image_likes[image_path] += 1
    return Text(f"{image_likes[image_path]} likes", id=f"likes-{image_path}", style="likes-count")

# route handler to handle likes
@rt('/invalid/like/{image_path}')
def get(image_path: str, req):
    if image_likes[image_path] > 0: image_likes[image_path] += 1
    return Text(f"{image_likes[image_path]} likes", id=f"likes-{image_path}", style="likes-count")

serve(port=8085)