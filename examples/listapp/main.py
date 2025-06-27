from fasthtml.common import database
from fastmobile import *
from datetime import datetime

db = database('goals.db')

goals = db.t.goals
if goals not in db.t: goals.create(id=int, title=str, type=str, created_at=datetime, done=bool, pk='id')

Goal = goals.dataclass()
app, rt = fast_app()

sty = Styles(
    Style('body', fontSize=16, padding='t16 b16 l12 r12', backgroundColor='#F8FAFC', width='100%', height='100%'),
    Style('title', fontSize=34, fontWeight='700', color='#1F2937', margin='t16 b24'),
    Style('goal-txt', fontSize=16, fontWeight='500', color='#1F2937'),
    Style('btn', backgroundColor='#2563EB', borderRadius=10, padding='t14 b14 l20 r20', alignItems='center', justifyContent='center'),
    Style('btn-txt', color='#FFFFFF', fontSize=16, fontWeight='600'),
    Style(Modifier(pressed='true'), 'btn-pressed', backgroundColor='#1E40AF'),
    Style('btn-ct', flexDirection='row', justifyContent='space-between', margin='t24'),
    Style('goals-container', margin='b24'),
    Style('goal-row',
          flexDirection='row',
          justifyContent='space-between',
          alignItems='center',
          padding=12,
          margin='b8',
          backgroundColor='#FFFFFF',
          borderRadius=8,
          borderWidth=1,
          borderColor='#E5E7EB',
          shadowColor='#000000',
          shadowOpacity=0.05,
          shadowRadius=4,
          shadowOffsetY=2,
          elevation=1),
    Style('txt-input',
          backgroundColor='#FFFFFF',
          borderRadius=8,
          padding='t14 b14 l20 r20',
          margin='t24 b24',
          borderWidth=1,
          borderColor='#E5E7EB')
)

def Button(text, href=None, action='push', **kwargs):
    button = View(style='btn btn-pressed')(
        Text(text, style='btn-txt'),
        **kwargs)
    if not href: return button
    return View(Behavior(trigger='press', href=href, action=action), button)

def NavBtns(prev, next):
    return  View(style='btn-ct')(
        Button('Back', href=prev),
        Button('Next', href=next))

def mk_input(typ='y'): return TextField(id=f'txt-input-{typ}', name='txt', value='', placeholder='Enter your goals', style='txt-input')

def mk_form(typ='y'):
    return Form(
        mk_input(typ),
        View(
            Button('Add Goal', id='submit-btn'),
            Behavior(trigger='press', href=f'/add-{typ}',         action='replace', target=f'list-{typ}'),
            Behavior(trigger='press', href=f'/clear-input-{typ}', action='replace', target=f'txt-input-{typ}')))

def mk_list(typ='y', msg=None):
    return View(id=f'list-{typ}')(
        *[
            View(style='goal-row')(
                Text(goal.title, style='goal-txt'),
                View(
                    Button('X'),
                    Behavior(trigger='press', href=f'/delete-{typ}/{goal.id}', action='replace', target=f'list-{typ}')
                ), 
            ) for goal in goals('type = ?', [typ], order_by='created_at')
        ], 
        View(msg, hide=msg is None))

@rt('/')
def get(): return StackNav(NavRoute(href='show-y', id='y')) # Doc

@rt('/show-{typ}')
def get(typ:str):
    title, prev, next = {
        'y': ('Your Yearly Goals',    'm', 'w'),
        'q': ('Your Quarterly Goals', 'w', 'y'),
        'w': ('Your Weekly Focus',    'y', 'm')
    }[typ]
    return Screen(
        sty,
        Body(style='body')(
            View(Text(title, style='title')),
            mk_list(typ=typ),
            mk_form(typ),
            NavBtns(f'/show-{prev}', f'/show-{next}')))

@rt('/add-{typ}') 
def get(txt:str, typ:str):
    limit = {'y': 3, 'q': 5, 'w': 3}
    count = len(list(goals('type = ?', [typ])))
    if count >= limit[typ]:
        typ_long = {'y': 'yearly', 'q': 'quarterly', 'w': 'weekly'}
        msg = f'Keep it simple! You can only add {limit[typ]} {typ_long[typ]} goals.'
        return mk_list(typ, msg)
    goals.insert(Goal(title=txt, type=typ, created_at=datetime.now().isoformat(), done=False))
    return mk_list(typ)

@rt('/delete-{typ}/{id}')
def get(id:int, typ:str):
    goals.delete(id)
    return mk_list(typ)

@rt('/clear-input-{typ}')
def get(typ:str): return mk_input(typ)

serve(port=8085)