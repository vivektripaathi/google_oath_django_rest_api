import orjson

from typing import Dict, Union, cast
from pydantic import BaseModel
from pydantic.generics import GenericModel

def _dict_serialized(obj: Union[BaseModel, GenericModel], *args, **kwargs) -> Dict:
    """
    Returns a dict of serialized data. We need this because
    pydantic's .json() returns stringified json, we need
    a dict to return it as a response.
    """
    return cast(Dict, orjson.loads(obj.json(*args, **kwargs)))


class OrderlyAuthBaseModel(BaseModel):
    """Orderly Auth Base Model from which all other Models should inherit"""

    def dict_serialized(self, *args, **kwargs) -> Dict:
        return _dict_serialized(self, *args, **kwargs)
