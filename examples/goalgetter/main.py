from fasthtml.common import database
from fastmobile import *
from datetime import datetime

db = database('goals.db')

goals = db.t.goals
if goals not in db.t:
    goals.create( id=int, title=str, type=str, created_at=datetime, done=bool, pk='id')

Goal = goals.dataclass()
app, rt = fast_app()

sty = Styles(
    Style("base", fontSize=24, padding=24),
    Style("screen-title",
        fontSize=32,              # Larger font for emphasis
        fontWeight="700",         # Bold weight for prominence
        color="#1a1a1a",         # Dark gray, not pure black for softer look
        marginBottom=24,          # Good spacing below title
        marginTop=12             # Some space at top
    ),
    Style("gl-txt",
        fontSize=32,              # Larger font for emphasis
        fontWeight="500",         # Bold weight for prominence
        color="#1a1a1a",         # Dark gray, not pure black for softer look
        marginBottom=4,          # Good spacing below title
        marginTop=4             # Some space at top
    ),
    Style(id="Button", 
        backgroundColor="#4778FF",
        borderRadius=8,
        padding=16,
        alignItems="center",
        justifyContent="center"
    ),
    Style(id="Button__Text",
        color="white", 
        fontSize=16,
        fontWeight="bold"
    ),
    Style(Modifier(pressed="true"),
        id="Button__Pressed",
        backgroundColor="#2955CC",
    ),
    Style("btn-ct",
        flexDirection="row",
        gap=210,  # Space between buttons
        # gap=16,  # Space between buttons
        marginTop=16  # Optional top margin
    ),
    Style('container',
        margin='36 12 12 12'),
    Style('bdy-full', 
        width='100%',
        height='100%'
    ),
    Style("goals-container",
        marginBottom=24
    ),
    Style("goal-row",
    flexDirection="row",
    justifyContent="space-between", 
    alignItems="center",
    padding="4",
    marginBottom="8",  # Increased for better spacing
    backgroundColor="#ffffff",  # White background
    borderRadius="12",  # Increased roundness
    borderWidth="1",  # Add subtle border
    borderColor="#e5e7eb", # Light gray border
    shadowColor="#000000",  # Add subtle shadow
    shadowOpacity=0.1,
    shadowRadius=8,
    shadowOffsetY=2
)
)

def Button(text, href=None, action="push", **kwargs):
    button = View(
        Text(text, style="Button__Text"),
        style="Button Button__Pressed",
        **kwargs
    )

    if href:
        return View(
            Behavior(trigger="press", href=href, action=action),
            button)
    return button

def NavBtn(href_f, href_b):
    return  View(Button('Back', href=href_b),
                 Button('Next', href=href_f),
                 style="btn-ct")

def mk_frm(txt_fld="yearly"):
    if txt_fld=="yearly":
        name="yearly_goal" 
        placeholder="Enter your yearly goals"
        _id="y-txt-fld"
        href="/add-yearly-goal"
        target="yg-lst"
        clhref = '/y-clear-input'

    elif txt_fld=="quarterly":
        name="quarterly_goal" 
        placeholder="Enter your goals for the next quarter"
        _id="q-txt-fld"
        href="/add-quarterly-goal"
        target="qg-lst"
        clhref = '/q-clear-input'

    elif txt_fld=="weekly":
        name = "weekly_goal" 
        placeholder="Enter your weekly targets"
        _id="w-txt-fld"
        href="/add-weekly-goal"
        target="wg-lst"
        clhref = '/w-clear-input'

    return Form(style="base")(
        TextField(name=name, placeholder=placeholder,id=_id,style="base"),
        View(Button("Add Goal", id='submit-btn'),
            Behavior(trigger="press", href=href,   action="replace", target=target ),
            Behavior(trigger="press", href=clhref, action="replace", target=_id ),
        )
    )

def mk_yglst(msg=None, gl_type='yearly'):
    hide_vw = "false" if msg else "true"
    if gl_type=="yearly":
        _id = 'yg-lst'
        dhref = f"/delete-y/"
    elif gl_type=="quarterly":
        _id = 'qg-lst'
        dhref = f"/delete-q/"
    elif gl_type=="weekly":
        _id = 'wg-lst'
        dhref = f"/delete-w/"

    return View(*[
        View(
            View(Text(goal.title, style="gl-text")),
            View(style="goal-row")(
                Button("X"),
                Behavior( trigger="press", href=dhref+str(goal.id), action="replace", target=_id )
            ), 
        ) for goal in goals('type = ?', [gl_type], order_by='created_at')
    ], View(msg, hide=hide_vw, style="base"), id=_id, style="base")


@rt('/')
def get():
    return Doc(StackNav(NavRoute(href='tab-1', id='tab-1')))

@rt('/tab-1')
def get():
    yearly_goals = list(goals('type = ?', ['yearly'], order_by='created_at'))
    return Screen(
               sty,
               Body(
                   View(Text('Your Yearly Goals', style="screen-title")),
                   mk_yglst(),
                   mk_frm(txt_fld="yearly"),
                   NavBtn('/tab-2', '/tab-3'),
                   style="base"))

@rt('/tab-2')
def get():
    quarterly_goals = list(goals('type = ?', ['quarterly'], order_by='created_at'))
    return Screen(
                sty,
                Body(
                    View(Text('Your Quarterly Goals', style="screen-title")),
                    mk_yglst(gl_type='quarterly'),
                    mk_frm(txt_fld="quarterly"),
                    NavBtn('/tab-3', '/tab-1'),
                    scroll='true',
                    style="base"))

@rt('/tab-3')
def get():
    weekly_goals = list(goals('type = ?', ['weekly'], order_by='created_at'))
    return Screen(
                sty,
                Body(
                    View(Text('Your Weekly Focus', style="screen-title")),
                    mk_yglst(gl_type="weekly"),
                    mk_frm(txt_fld="weekly"),
                    NavBtn('/tab-1', '/tab-2'),
                    style="base"))

@rt('/add-yearly-goal') 
def get(yearly_goal: str):
    count = len(list(goals('type = ?', ['yearly'])))
    if count >= 3: return View(mk_yglst("You Cannot Add More Than 3 Yearly Goals!!!"))
    goals.insert(Goal( title=yearly_goal, type='yearly', created_at=datetime.now().isoformat(), done=False ))
    return mk_yglst()
    
@rt('/add-quarterly-goal') 
def get(quarterly_goal: str):
    count = len(list(goals('type = ?', ['quarterly'])))
    if count >= 5: return View(mk_yglst("You Cannot Add More Than 5 Quarterly Goals!!!", gl_type='quarterly'))
    goals.insert(Goal( title=quarterly_goal, type='quarterly', created_at=datetime.now().isoformat(), done=False ))
    return mk_yglst(gl_type="quarterly")

@rt('/add-weekly-goal') 
def get(weekly_goal: str):
    count = len(list(goals('type = ?', ['weekly'])))
    if count >= 3: return View(mk_yglst("You cannot add more than 3 weekly targets!", gl_type='weekly'))
    goals.insert(Goal(title=weekly_goal, type='weekly', created_at=datetime.now().isoformat(), done=False))
    return mk_yglst(gl_type="weekly")

@rt('/delete-y/{goal_id}')
def get(goal_id: int):
    goals.delete(goal_id)
    return mk_yglst(gl_type="yearly")

@rt('/delete-q/{goal_id}')
def get(goal_id: int):
    goals.delete(goal_id)
    return mk_yglst(gl_type="quarterly")   
    
@rt('/delete-w/{goal_id}')
def get(goal_id: int):
    goals.delete(goal_id)
    return mk_yglst(gl_type="weekly")   

@rt('/y-clear-input')
def get(): return TextField(name="yearly_goal",    placeholder="Enter your goals", id="y-txt-fld", style="base")
@rt('/q-clear-input')
def get(): return TextField(name="quarterly_goal", placeholder="Enter your goals", id="q-txt-fld", style="base")
@rt('/w-clear-input')
def get(): return TextField(name="weekly_goal",    placeholder="Enter your goals", id="w-txt-fld", style="base")

serve(port=8085)