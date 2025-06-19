# todo:
# - styling
#   - default styling for doc
#   - easier styling
#   - possible to define styles in a component? otherwise components not possible
#   - styling: err as state, like focused?
#   - convencience for borderColor, similar to margin/padding?
#   - auto-flex = 1 body,view,img; also in href-style?
#   - of only single a, else kw: if a str, then style?
# - auto add navigator (when?)
# - local caching?
# - parse str to txt when creating FT via curry
# ! auto add href_style that inherits some layout styles

import types
from functools import partial
from pathlib import Path
from starlette.responses import Response
from fastcore.basics import camel2words
from fastcore.xml import FT, _flatten_tuple
from fasthtml.core import _part_resp, _to_xml, flat_tuple, fh_cfg
from fasthtml.fastapp import fast_app as fh_fast_app
from fasthtml.common import *


# # Create tags
def _fix_k(o): return o.lstrip('_').replace('_','-')
def _fix_v(o): return str(o).lower() if isinstance(o,bool) else o

def _id_from_str(t,c,kw):
    if len(c)>0 and isinstance(c[0], str): kw['id'],c = c[0],c[1:]
    return t,c,kw

def _expand_spacing(s):
    xs = str(s).split()
    if any(o[0] in 'trbl' for o in xs): return {o[0]: int(o[1:]) for o in xs}        
    xs = [int(o) for o in xs]
    xs = {1:xs*4, 2:xs*2, 3:xs+xs[1:2], 4:xs}[len(xs)]
    return dict(zip('trbl', xs))
def _spacing(prefix, o):
    nms = {o[0]:prefix+o.capitalize() for o in ['top','right','bottom','left']}
    return {nms[k]:v for k,v in _expand_spacing(o).items()}
def _expand_margin_padding(t,c, kw):
    m,p = kw.pop('margin', None), kw.pop('padding', None)
    m = _spacing('margin',  m) if m else {}
    p = _spacing('padding', p) if p else {}
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

def _add_default_key(t,c,kw):
    if 'id' in kw and 'key' not in kw: kw['key'] = kw['id']
    return t,c,kw

def _preproc(t, c, kw):
    if len(c)==1 and isinstance(c[0], (types.GeneratorType, map, filter)): c = tuple(c[0])
    kw = {_fix_k(k): _fix_v(v) for k,v in kw.items()}
    tfms = {
        'styles': [_parse_style_dict],
        'style':  [_id_from_str, _expand_margin_padding],
        'image':  [_expand_src, _parse_svg],
        'item':   [_add_default_key]
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
    'Form', 'TextField', 'SelectSingle', 'SelectMultiple', 'Option',
    'Styles', 'Style', 'Modifier',
    'Navigator', 'NavRoute'
]
for o in tags: globals()[o] = partial(ft_hxml, hxml_name(o))

# # Convenience functions
def WhenFocused (**kw): return Modifier(focused ='true')(Style(**kw))
def WhenSelected(**kw): return Modifier(selected='true')(Style(**kw))
def WhenPressed (**kw): return Modifier(pressed ='true')(Style(**kw))
def StackNav(*c): return Navigator(_id='root', type='stack')(*c)
def TabNav(*c):   return Navigator(_id='root', type='tab')  (*c)
def Empty(): return Text('', hide=True)
def Back(**kw): return Behavior(action='back',**kw)
def Dispatch(event_name, **kw): return Behavior(action='dispatch-event', event_name=event_name, **kw)
def On      (event_name, **kw): return Behavior(trigger='on-event',      event_name=event_name, **kw)
def DispatchBack(event_name):
    return View(
        Dispatch(event_name=event_name, trigger='load'),
        Back(trigger='load'))
conveniences = 'WhenFocused WhenSelected WhenPressed StackNav TabNav Empty Back Dispatch On DispatchBack'.split(' ')

# # Return HXML
def is_fragment_request(req): return 'fragment' in req.headers.get('accept', '')
def is_full_doc(o): return len(o)==1 and o[0].tag=='doc'

def _to_hxml_response(resp, req):
    "After-ware: turn any FT tree into a Hyperview XML `Response`."
    if isinstance(resp, Response):  return resp
    # Pull out background tasks and extra headers
    bdy, kw = _part_resp(req, resp)
    hdrs = kw.get('headers', {})
    background = kw.get('background', None)
    bdy = flat_tuple(bdy)
    # Hyperview rules
    if resp and not is_fragment_request(req) and not is_full_doc(bdy):
        # todo: build support for header/footer back in. how do these relate to screen?
        if not any(getattr(o, 'tag', '')=='screen' for o in bdy): bdy = Screen(*bdy)
        bdy = Doc(bdy, **req.htmlkw)
    else:
        bdy = View(*resp) if len(bdy)>1 else bdy[0]
    bdy.xmlns = 'https://hyperview.org/hyperview'
    xml = '<?xml version="1.0" encoding="UTF-8"?>' + _to_xml(req, bdy, indent=fh_cfg.indent)
    return Response(xml, media_type='application/xml', headers=hdrs, background=background)

def fast_app(*a, **kw):
    app, *rest = fh_fast_app(*a, **kw, default_hdrs=False)
    app.after.append(_to_hxml_response)
    return app,*rest

__all__ = tags + conveniences + ['fast_app', 'serve']
