from typing import Any, Callable, Dict, Generator, Iterator, List, Optional, Tuple, Union, TypeVar, overload
from types import GeneratorType
from starlette.responses import Response
from starlette.requests import Request
from starlette.background import BackgroundTask, BackgroundTasks

T = TypeVar('T')

# Core types
class FT:
    tag: str
    def __init__(self, tag: str, *children: Any, **attributes: Any) -> None: ...
    def __call__(self, *children: Any, **attributes: Any) -> 'FT': ...

# Helper functions
def margin(spacing: Union[str, int]) -> Dict[str, int]: ...
def padding(spacing: Union[str, int]) -> Dict[str, int]: ...

# Main XML response
def XMLResponse(
    content: Any,
    status_code: int = 200,
    headers: Optional[Dict[str, str]] = None,
    media_type: str = 'application/xml',
    background: Optional[BackgroundTasks] = None
) -> Response: ...

# Core functions
def fast_app(
    db_path: str,
    *,
    id: Any = None,
    title: Any = None,
    done: Any = None,
    pk: str = 'id'
) -> Tuple[Any, Any, Any, Any]: ...

def serve(
    app: Any,
    host: str = 'localhost',
    port: int = 8000,
    log_level: str = 'info',
    reload: bool = True
) -> None: ...

# Navigation components
def StackNav(*children: Any) -> FT: ...
def TabNav(*children: Any) -> FT: ...
def Navigator(
    _id: str = 'root',
    type: str = 'stack',
    **kwargs: Any
) -> FT: ...
def NavRoute(**kwargs: Any) -> FT: ...

# UI Components
def Doc(*children: Any, **kwargs: Any) -> FT: ...
def Screen(*children: Any, **kwargs: Any) -> FT: ...
def Header(*children: Any, **kwargs: Any) -> FT: ...
def Body(*children: Any, **kwargs: Any) -> FT: ...
def View(*children: Any, **kwargs: Any) -> FT: ...
def Text(*children: Any, **kwargs: Any) -> FT: ...
def Img(*children: Any, src: Optional[str] = None, **kwargs: Any) -> FT: ...
def List(*children: Any, **kwargs: Any) -> FT: ...
def Item(*children: Any, **kwargs: Any) -> FT: ...
def Spinner(*children: Any, **kwargs: Any) -> FT: ...

# Form components
def Form(*children: Any, **kwargs: Any) -> FT: ...
def TextField(*children: Any, **kwargs: Any) -> FT: ...
def TextArea(*children: Any, **kwargs: Any) -> FT: ...
def SelectSingle(*children: Any, **kwargs: Any) -> FT: ...
def SelectMultiple(*children: Any, **kwargs: Any) -> FT: ...
def Option(*children: Any, **kwargs: Any) -> FT: ...

# Section components
def SectionList(*children: Any, **kwargs: Any) -> FT: ...
def SectionTitle(*children: Any, **kwargs: Any) -> FT: ...

# Styling components
def Styles(*children: Any, **kwargs: Any) -> FT: ...
def Style(*children: Any, **kwargs: Any) -> FT: ...
def Modifier(*children: Any, focused: str = 'true', **kwargs: Any) -> FT: ...
def WhenFocused(**kwargs: Any) -> FT: ...

# Behavior
def Behavior(*children: Any, **kwargs: Any) -> FT: ...

# Internal helpers exposed in __all__
def is_fragment_request(req: Request) -> bool: ...
def is_full_doc(obj: Any) -> bool: ...