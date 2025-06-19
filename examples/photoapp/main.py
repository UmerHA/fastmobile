"""
TODO: 
    - Like/Dislike von Photos
    - Mit Kamera Foto machen und bei den anderen Fotos speichern - Nicht möglich

"""
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
for p in PIC:
    image_likes[str(p)] = random.randint(5, 100)

app, rt = fast_app()

sty = Styles(
    Style("base",
        fontSize=24
    ),
    Style("pad",
        paddingLeft=24,
    ),
    Style("list-container",
        flex=1,
        paddingBottom=280  # Same as image height
    ),
    Style("scroll-container",
        flex=1
    ),
    Style("image",
        height=375,
        width=375,
        flex=1,
    ),
    Style("image-container",
        alignItems="center",  # Centers children horizontally
        width="100%"  # Takes full width so centering works
    ),
    Style("stories",
        backgroundColor="#F4F4F4",
        flex=1,
        flexDirection="row", # Make children flow horizontally 
        paddingLeft=8
    ),
    Style("story",
        alignItems="center",
        flex=1,
        marginLeft=8,
        marginRight=8,
        marginTop=26,
        marginBottom=18
    ),
    Style("story-avatar", 
        backgroundColor="#F4F4F4",
        borderRadius=32,
        height=64,
        width=64
    ),
    Style("story-username",
        fontSize=14,
        fontWeight="bold", 
        marginTop=4
    ),
        Style("image-header",
        alignItems="center",
        backgroundColor="white",
        flex=1,
        flexDirection="row",
        justifyContent="space-between",
        paddingBottom=16,
        paddingLeft=16,
        paddingRight=16,
        paddingTop=16
    ),
    Style("image-header-avatar",
        backgroundColor="#F4F4F4",
        borderRadius=34,
        height=50,
        width=50,
        marginTop=10,
        marginBottom=10,
        marginLeft=5,
    ),
    Style("image-header-left",
        flexDirection="row"
    ),
    Style("image-header-left-labels",
        justifyContent="center",
        marginLeft=8
    ),
    Style("image-header-username",
        color="#4E4D4D",
        fontSize=14,
        fontWeight="bold"
    ),
    Style("image-header-location",
        color="#BDC4C4",
        fontSize=14,
        fontWeight="normal"
    ),
    Style("image-header-right",
        flexDirection="row"
    ),
    Style("image-header-more",
        color="#BDC4C4",
        fontSize=14,
        fontWeight="bold"
    ),
    Style("back",
        flex=1,
        padding=15,  # This adds 15px of padding around all sides
        width=24,
        height=24
        # marginLeft=8,
        # marginRight=8,
        # marginTop=26,
        # marginBottom=18
    ),
    Style("back-btn",
        # padding=35,  # This adds 15px of padding around all sides
        # marginLeft=8,
        # marginRight=8,
        # marginTop=26,
        # marginBottom=18
        padding=10,  # This adds 15px of padding around all sides
        marginLeft=2,
        marginRight=4,
        marginTop=16,
        marginBottom=8
    ),
    Style("center-txt",
        fontSize="24",
        fontWeight="bold",
        textAlign="center",
        alignItems="center",
        justifyContent="center",
        flex="1",
        position="absolute",
        top="30",
        bottom="0",
        left="0" ,
        right="0"
    ),
    Style("username",
        paddingBottom="20",
        marginBottom="15"
    ),
    Style("line",
        backgroundColor="#808080",
        height="2",
        width="90%",
        marginLeft="5%",
        marginRight="5%"
    ),
    Style("profile-stats",
        flexDirection="row",
        justifyContent="space-around",
        paddingTop=20,
        paddingBottom=20,
        width="80%"
    ),
    Style("stat-column",
        alignItems="center"
    ),
    Style("stat-number",
        fontSize=18,
        fontWeight="bold"
    ),
    Style("stat-label",
        fontSize=14,
        color="#666666"
    ),
    Style("profile-pic",
        width=60,
        height=60,
        borderRadius=30,
        marginTop=15,
        marginBottom=15
    ),
    Style("profile-section",
        flexDirection="row",
        alignItems="center",
        paddingHorizontal=15,
        width="100%"
    ),
    Style("bio-section",
    paddingHorizontal=20,
    marginTop=10,
    marginBottom=20,
    ),
    Style("bio-name",
        fontSize=14,
        fontWeight="bold",
        marginBottom=4,
    ),
    Style("bio-text",
        fontSize=14,
        color="#262626",
    ),
    Style("image-grid",
        flexDirection="row",
        flexWrap="wrap",
        width="100%",
    ),
    Style("grid-image",
        width="33.33%",  # Take up one-third of the width
        aspectRatio=1,   # Make it square
        padding=1,       # Small gap between images
    ),
    Style("grid-image-inner",
        width="100%",
        height="100%",
        backgroundColor="#EFEFEF",  # Light gray background while loading
    ),
    Style("likes-count",
        fontSize=14,
        fontWeight="bold",
        marginTop=8,
        marginLeft=16,
        color="#4E4D4D"
    ),
    Style("actionbar",
        flexDirection="row",
        justifyContent="space-between",
        marginLeft=16,
        marginRight=16,
        marginTop=8,
    ),
    Style("actionbar-left", 
        flexDirection="row"
    ),
    Style("heart-icon",
        width=24,
        height=24,
        marginRight=8
    )
)

def head():
    return View(
            (View(
                (Img(source=u.file,  href=f"/up/{u.uid}", style="story-avatar"), 
                 Text(u.name, numberOfLines="1", href=f"/up/{u.uid}", style="story-username")), 
            style="story") for u in usr_lst),
            scroll="true", scroll_orientation="horizontal")

def card(u):
    return View(
        View(
             Img(source=u.file, style="image-header-avatar"),
             View(
                Text(u.name, style="image-header-username"),
                Text(u.loc, style="image-header-location"),
                style="image-header-left-labels"
             ),
        style="image-header-left",
        )
    )

def lst_vw():
    return View(
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
        ),
        style="list-container"
    )

@rt('/')
def get():
    return Doc(StackNav(NavRoute(href="/home", id="home")))

@rt('/home')
def get():
    return sty, Body(View(head(), View(lst_vw(), scroll="true")))

@rt('/up/{uid}')
def get(uid: int):
    u = usr_lst[uid]
    return sty, Body(
        View(
            View(Text(u.name, style="center-txt"), View(Img(source="icons/back.svg", style="back"), href="/home", action="back", style="back-btn"), style="username"),
            View(style="line"),
            View(
                Img(source=u.file, style="profile-pic"),
                View(
                    View(
                        Text(f"{u.posts}", style="stat-number"),
                        Text("posts", style="stat-label"), 
                        style="stat-column"
                    ),
                    View(
                        Text(f"{u.follower}", style="stat-number"),
                        Text("followers", style="stat-label"),
                        style="stat-column" 
                    ),
                    View(
                        Text(f"{u.following}", style="stat-number"), 
                        Text("following", style="stat-label"),
                        style="stat-column"
                    ),
                    style="profile-stats"
                ), style="profile-section"
            ), 
            View(
                Text(u.name.upper(), style="bio-name"),
                Text("I'm a synthetic life form with artificial intelligence.\nLove long walks on the beach and pumpkin spice everything!", 
                     style="bio-text"),
                style="bio-section"
            ),
            View(
                *(View(
                    Img(source=img, 
                        style="grid-image-inner"),
                    style="grid-image"
                  ) for img in u.img_lst[:]),
                style="image-grid"
            )
    ))
    
# route handler to handle likes
@rt('/like/test')
def get():
    # Toggle the like status
    image_path=PIC[-1]
    print(image_path)
    print("likes:")
    print(image_likes[image_path])

    # if image_likes[image_path] > 0:
    image_likes[image_path] += 1
    return Text(f"{image_likes[image_path]} likes", id=f"likes-{image_path}", style="likes-count")

# route handler to handle likes
@rt('/like/{image_id}')
def get(image_id: int):
    
    print("Geschafft! Works!")
    image_path = str(PIC[int(image_id)])

    image_likes[image_path] += 1
    # Return the updated like count
    return Text(f"{image_likes[image_path]} likes", id=f"likes-{image_path}", style="likes-count")

# route handler to handle likes
@rt('/invalid/like/{image_path}')
def get(image_path: str, req):
    # Toggle the like status
    if image_likes[image_path] > 0:
        image_likes[image_path] += 1
    
    # Return the updated like count
    return Text(f"{image_likes[image_path]} likes", id=f"likes-{image_path}", style="likes-count")

serve(port=8085)