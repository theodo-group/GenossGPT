"""This is highly inspired from starlette.routing.

The goal is to have a ModelRouter that can be used to register models and their routes.
We stick to the starlette.routing API as much as possible to have a known interface.

For the moment, we do not handle nested routes.
"""
import re
from abc import ABC, abstractmethod
from collections.abc import Sequence
from typing import Any, Generic, TypeVar

from pydantic import BaseModel, Field, ValidationError, root_validator
from starlette.convertors import Convertor
from starlette.routing import Match, compile_path

from genoss.llm.base_genoss import BaseGenossLLM


class RouterException(Exception):
    pass


class InvalidRouteParameters(ValueError, RouterException):
    pass


class RouteNotFound(ValueError, RouterException):
    pass


ModelT = TypeVar("ModelT", bound=BaseGenossLLM)
RouteParams = dict[str, Any]
CallParams = dict[str, Any]


class AbstractRoute(ABC):
    """The abstract route.

    Similar to : from starlette.routing import BaseRoute.
    """

    @abstractmethod
    def matches(self, route: str) -> tuple[Match, RouteParams]:
        raise NotImplementedError()

    @abstractmethod
    def handle(self, call_params: CallParams, route_params: RouteParams) -> Any:
        raise NotImplementedError()


class StandardModelRoute(AbstractRoute, Generic[ModelT], BaseModel):
    """A route for a specific model.

    Similar to : from starlette.routing import Route
    """

    path: str
    model_class: type[ModelT]
    additional_params: RouteParams = Field(default_factory=dict)
    regex: re.Pattern[str]
    formatted_route: str
    converters: dict[str, Convertor[Any]]
    call_params_keys: set[str]

    class Config:
        # Necessary to allow converters with pydantic
        arbitrary_types_allowed = True

    @classmethod
    def from_route_and_model(
        cls,
        path: str,
        model_class: type[ModelT],
        additional_params: RouteParams | None = None,
        call_params_keys: set[str] | None = None,
    ) -> "StandardModelRoute[ModelT]":
        if additional_params is None:
            additional_params = {}
        if call_params_keys is None:
            call_params_keys = set()
        regex, formatted_route, converters = compile_path(path)
        return cls(
            path=path,
            model_class=model_class,
            additional_params=additional_params,
            regex=regex,
            formatted_route=formatted_route,
            converters=converters,
            call_params_keys=call_params_keys,
        )

    @root_validator(skip_on_failure=True)
    def validate_route(cls, values: dict[str, Any]) -> dict[str, Any]:
        available_params_at_handle = set(values["converters"].keys()) | set(
            values["additional_params"].keys()
        )
        call_params_keys = values["call_params_keys"]
        model_class = values["model_class"]
        model_fields = model_class.__fields__
        required_fields = {
            name for name, field in model_fields.items() if field.required
        }

        non_existing_fields = available_params_at_handle - model_fields.keys()
        if non_existing_fields:
            raise ValueError(
                f"Route variables {non_existing_fields} do not exist in model: {model_class}."
            )
        if required_fields - available_params_at_handle - call_params_keys:
            raise ValueError(
                f"Required fields {required_fields} are not "
                f"in route variables: {available_params_at_handle} "
                f"or call_params_keys: {call_params_keys}."
            )
        return values

    def matches(self, path: str) -> tuple[Match, RouteParams]:
        # See later to implement partial routing
        match = self.regex.match(path)
        if match is None:
            return Match.NONE, {}
        matched_params = match.groupdict()
        converted_params = {
            key: self.converters[key].convert(value)
            for key, value in matched_params.items()
        }
        return Match.FULL, converted_params

    def handle(self, call_params: CallParams, route_params: RouteParams) -> ModelT:
        """Create the Model (__init__) from all the params.

        There are 4 types of parameters that will enter the `model_class.__init__`.
        - route_params (from the route).
          Example: "openai/{model_name:str}-{version:str}" with "openai/gpt-4-0314"
          should result in {"model_name": "gpt-4", "version": "0314"}.
        - additional_params which comes from registering the route.
          Example:```python
              embeddings.register_model(
                "openai/gpt-4",
                OpenAILLM,
                additional_params={"model_name": "gpt-4-0314"},
                call_params={"api_key"}
              )
              ```
        - default values from the model init which does not appear here
          as they are handled by the model class itself.
        - handle_time_params which are params that are not in the route
          but are added at handle time.
        """
        try:
            if call_params.keys() != self.call_params_keys:
                # TODO: create a stronger signature / type system ?
                raise TypeError(
                    f"call_params should contain the same keys than call_params_keys "
                    f"{call_params} != {self.call_params_keys}."
                )
            return self.model_class(
                **call_params, **route_params, **self.additional_params
            )
        except ValidationError as exception:
            # TODO: We should probably think about a better exception
            # that will raise a validation issue to genoss client.
            # Examples could be, the model is not available
            # for your current API key,
            # or the model is not available anymore (deprecation).
            raise InvalidRouteParameters(
                f"Failed to instantiate the model {self.model_class.__name__} "
                f"from the provided parameters {call_params} {route_params} and {self.additional_params}."
            ) from exception


class ModelRouter(Generic[ModelT], BaseModel):
    """The model router.

    Similar to : from starlette.routing import Router

    This is a model registry.
    You can call register to register a model.
    For example :
    ```python
    chat_completion = ModelRouter()
    chat_completion.register(["{model_name:str}", "openai/{model_name:str}"], OpenAILLM)
    chat_completion.register(
       "openai",
       OpenAILLM,
       additional_params={"model_name": "gpt-3.5-turbo"}
    )

    instantiated_model = chat_completion.build_model("openai", {"api_key": "1234"})
    instantiated_model.generate_answer("What is the meaning of life?")
    ```
    """

    routes: list[StandardModelRoute[ModelT]] = Field(default_factory=list)

    def register_model(
        self,
        paths: str | Sequence[str],
        model_class: type[ModelT],
        additional_params: RouteParams | None = None,
        call_params_keys: set[str] | None = None,
    ) -> None:
        if additional_params is None:
            additional_params = {}
        if call_params_keys is None:
            call_params_keys = set()
        if isinstance(paths, str):
            paths = [paths]

        for path in paths:
            route = StandardModelRoute.from_route_and_model(
                path=path,
                model_class=model_class,
                additional_params=additional_params,
                call_params_keys=call_params_keys,
            )
            self.routes.append(route)

    def build_model(self, path: str, call_params: CallParams) -> ModelT:
        for route in self.routes:
            match, route_params = route.matches(path)
            if match is Match.FULL:
                return route.handle(call_params, route_params)
        # TODO: better error type
        raise RouteNotFound(f"No model found for path: {path}")
