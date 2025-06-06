from typing import Any, Mapping, Optional, cast

from rest_framework import renderers


class PydanticRenderer(renderers.JSONRenderer):
    def render(
        self,
        data: Any,
        accepted_media_type: Optional[str] = None,
        renderer_context: Optional[Mapping[str, Any]] = None,
    ) -> bytes:
        from core.utils import OrderlyAuthBaseModel

        if isinstance(data, OrderlyAuthBaseModel):
            return data.json().encode("utf-8")
        return cast(bytes, super().render(data, accepted_media_type, renderer_context))