from genoss.llm.base_genoss import BaseGenossLLM
from genoss.llm.fake_llm import FAKE_LLM_NAME, FakeLLM
from genoss.llm.hf_hub.base_hf_hub import BaseHuggingFaceHubLLM
from genoss.llm.hf_inference_endpoint.hf_inference_endpoint import (
    HuggingFaceInferenceEndpointLLM,
)
from genoss.llm.local.gpt4all import Gpt4AllLLM
from genoss.llm.openai_llm.openai_llm import OpenAILLM
from genoss.services.model_routing_helpers import ModelRouter

chat_completion_registry = ModelRouter[BaseGenossLLM]()
# Warning: matches is order dependent. The first match will be used.
chat_completion_registry.register_model(
    paths="gpt4all",
    model_class=Gpt4AllLLM,
    call_params_keys={"api_key"},
)
chat_completion_registry.register_model(
    paths=FAKE_LLM_NAME,
    model_class=FakeLLM,
    call_params_keys={"api_key"},
)
chat_completion_registry.register_model(
    paths=["{model_name:str}", "openai/{model_name:str}"],
    model_class=OpenAILLM,
    call_params_keys={"api_key"},
)
chat_completion_registry.register_model(
    # Path catches slashes hf-hub/username/repo_name
    # For example those are valid :
    # hf-hub/gpt-2 and hf-hub/tiiuae/falcon-40b
    paths=["hf-hub/{repo_id:path}"],
    model_class=BaseHuggingFaceHubLLM,
    call_params_keys={"api_key"},
)
chat_completion_registry.register_model(
    paths=["hf-inference-endpoint/{endpoint_url:path}"],
    model_class=HuggingFaceInferenceEndpointLLM,
    call_params_keys={"api_key"},
)
