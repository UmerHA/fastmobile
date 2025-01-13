# todo:
# - styling
#   - default styling for doc
#   - easier styling
#   - possible to define styles in a component? otherwise components not possible
#   - styling: err as state, like focused?
#   - convencience for borderColor, similar to margin/padding?
# - auto add navigator (when?)
# - local caching?

import types
from functools import partial
from pathlib import Path
from fastcore.basics import camel2words
from fastcore.xml import to_xml, FT, _flatten_tuple
from starlette.responses import Response
from fasthtml.common import *
import fasthtml.core as fhcore


# # Helpers
def patch_module(mod):
    def _inner(f):
        setattr(mod, f.__name__, f)
        return f
    return _inner

# # Create tags
def _fix_k(o): return o.lstrip('_').replace('_','-')
def _fix_v(o): return str(o).lower() if isinstance(o,bool) else o

def _id_from_str(t,c,kw):
    if len(c)>0 and isinstance(c[0], str): kw['id'],c = c[0],c[1:]
    return t,c,kw

def _expand_margin_padding(t,c, kw):
    m,p = kw.pop('margin', None), kw.pop('padding', None)
    m = margin(m)  if m else {}
    p = padding(p) if p else {}
    return t,c, {**kw, **m, **p}

def _wrap_str(t,c,kw):
    if not any(isinstance(o,str) for o in c): return t,c,kw
    c = tuple(Text(o) if isinstance(o,str) else o for o in c) 
    return t,c,kw

def _parse_style_dict(t,c,kw):
    if not (kw == {} and len(c)==1 and isinstance(c[0],dict)): return t,c,kw
    return t,tuple(Style(k, **v) for k,v in c[0].items()), {}

def _expand_src(t,c,kw):
        src = kw.pop('src',None)
        if src: kw['source'] = src
        return t,c,kw

def _parse_svg(t,c,kw):
    if not kw['source'].endswith('.svg'): return t,c,kw
    src = kw.pop('source')
    if src.startswith('/'): src = src[1:] # relative path on server
    svg = Path(src).read_text()
    return 'view',(NotStr(svg),)+c,kw

def _preproc(t, c, kw):
    if len(c)==1 and isinstance(c[0], (types.GeneratorType, map, filter)): c = tuple(c[0])
    kw = {_fix_k(k): _fix_v(v) for k,v in kw.items()}
    tfms = {
        'styles': [_parse_style_dict],
        'style':  [_id_from_str, _expand_margin_padding],
        'image':  [_expand_src, _parse_svg],
    }
    tfms = tfms.get(t, []) + ([_wrap_str] if t not in ['text','image'] else [])
    for o in tfms: t, c, kw = o(t, c, kw)
    return t, _flatten_tuple(c),kw

def ft_hxml(t, *c, **kw): return FT(*_preproc(t,c,kw))

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
def TabNav(*c):   return Navigator(_id='root', type='tab')  (*c)

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
def XMLResponse(o, *a, **kw):
    o = '<?xml version="1.0" encoding="UTF-8"?>' + to_xml(o)
    return Response(o, *a, media_type='application/xml', **kw)

@patch_module(fhcore)
def _xt_resp(req, resp):
    cts,http_hdrs,tasks = _xt_cts(req, resp)
    return XMLResponse(cts, headers=http_hdrs, background=tasks)

def is_fragment_request(req): return 'fragment' in req.headers['accept']
def is_full_doc(o): return len(o)==1 and o[0].tag=='doc'

@patch_module(fhcore)
def _xt_cts(req, resp):
    resp = flat_tuple(resp) # why did we need this?
    resp = resp + tuple(getattr(req, 'injects', ()))
    http_hdrs,resp = partition(resp, risinstance(HttpHeader))
    http_hdrs = {o.k:str(o.v) for o in http_hdrs}
    tasks,bdy = partition(resp, risinstance(BackgroundTask))
    ts = BackgroundTasks()
    for t in tasks: ts.tasks.append(t)
    if resp and not is_fragment_request(req) and not is_full_doc(resp):
        # todo: build support for header/footer back in. how do these relate to screen?
        if not any(getattr(o, 'tag', '')=='screen' for o in bdy): bdy = Screen(*bdy)
        resp = Doc(bdy, **req.htmlkw)
    else:
        resp = View(*resp) if len(resp)>1 else resp[0]
    if hasattr(resp,'__ft__'): resp = resp.__ft__()
    resp.xmlns='https://hyperview.org/hyperview'
    return fhcore._to_xml(req, resp, indent=fh_cfg.indent), http_hdrs, ts

__all__ = tags + ['WhenFocused', 'StackNav', 'TabNav', 'fast_app', 'serve']
