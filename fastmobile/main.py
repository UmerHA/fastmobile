# todo:
# - in dev: reload app, not reinstall
# - styling
#   - text color applied to body doesn't seem to propagate?
#   - default styling for doc
#   - easier styling
#   - possible to define styles in a component? otherwise components not possible
#   - css-calc?
#   - styling: err as state, like focused?
#   - convencience for borderColor, similar to margin/padding?
# - hxml can't display svgs?
# - auto add: Doc tag (when?), navigator (when?)
# - aid static file checker via adding .pyi file?

import types, inspect
from anyio import to_thread
from functools import partial, wraps
from fastcore.basics import patch, camel2words
from fastcore.xml import to_xml, FT, _flatten_tuple
from starlette.responses import Response
from fasthtml.common import FastHTML, serve, fast_app

# # Create tags
def _fix_k(o): return o.lstrip('_').replace('_','-')
def _fix_v(o): return str(o).lower() if isinstance(o,bool) else o

def _id_from_str(c,kw):
    if len(c)>0 and isinstance(c[0], str): kw['id'],c = c[0],c[1:]
    return c,kw

def _expand_margin_padding(c, kw):
    m,p = kw.pop('margin', None), kw.pop('padding', None)
    m = margin(m)  if m else {}
    p = padding(p) if p else {}
    return c, {**kw, **m, **p}

def _wrap_str(c,kw):
    if not any(isinstance(o,str) for o in c): return c,kw
    c = tuple(Text(o) if isinstance(o,str) else o for o in c) 
    return c,kw

def _preproc(t, c, kw):
    if len(c)==1 and isinstance(c[0], (types.GeneratorType, map, filter)): c = tuple(c[0])
    kw = {_fix_k(k): _fix_v(v) for k,v in kw.items()}
    if t=='style':
        c, kw = _id_from_str(c,kw)
        c, kw = _expand_margin_padding(c,kw)        
    if t!='text': 
        c, kw = _wrap_str(c,kw)
    if t=='image':
        src = kw.pop('src',None)
        if src: kw['source'] = src
    return _flatten_tuple(c),kw

def ft_hxml(t, *c, **kw): return FT(t,*_preproc(t,c,kw))

def hxml_name(o):
    if o=='Img': o='Image'
    return camel2words(o, space='-').lower() # TextArea -> text-area

tags = [
    'Behavior',
    'Doc', 'Screen', 'Header', 'Body', 'View', 'Text', 'Img', 'List', 'SectionList', 'SectionTitle', 'Item', 'Spinner',
    'Form', 'TextField', 'TextArea', 'SelectSingle', 'SelectMultiple', 'Option',
    'Styles', 'Style', 'Modifier',
    'Navigator', 'NavRoute'
]
_g = globals()
for o in tags: _g[o] = partial(ft_hxml, hxml_name(o))

# # Convenience functions
def WhenFocused(**kw): return Modifier(focused='true')(Style(**kw))
def StackNav(*c): return Navigator(_id='root', type='stack')(*c)

def _expand_spacing(s):
    xs = str(s).split()
    if any(o[0] in 'trbl' for o in xs): return {o[0]: int(o[1:]) for o in xs}        
    xs = [int(o) for o in xs]
    xs = {1:xs*4, 2:xs*2, 3:xs+xs[1:2], 4:xs}[len(xs)]
    return dict(zip('trbl', xs))
def _spacing(prefix, o):
    nms = {o[0]:prefix+o.capitalize() for o in ['top','right','bottom','left']}
    return {nms[k]:v for k,v in _expand_spacing(o).items()}
margin  = partial(_spacing, 'margin')
padding = partial(_spacing, 'padding')

# # Return xml
def XMLResponse(o):
    o.xmlns = 'https://hyperview.org/hyperview'
    o = '<?xml version="1.0" encoding="UTF-8"?>' + to_xml(o)
    return Response(o, media_type='application/xml')

def make_xml_response(f):
    @wraps(f)
    async def _f(*a, **kw):
        o = await (f(*a, **kw) if inspect.iscoroutinefunction(f) else to_thread.run_sync(f, *a, **kw))
        return XMLResponse(o) if isinstance(o, FT) else o
    return _f

@patch
def route(self:FastHTML, path:str=None, methods=None, name=None, include_in_schema=True, body_wrap=None):
    "Add a route at `path`"
    def f(func): 
        func = make_xml_response(func)
        return self._add_route(func, path, methods, name=name, include_in_schema=include_in_schema, body_wrap=body_wrap)
    return f(path) if callable(path) else f

# # Other
@patch
def append(self:FT, c):
    self.children = self.children + (c,)

__all__ = tags + ['WhenFocused', 'StackNav', 'fast_app', 'serve']
