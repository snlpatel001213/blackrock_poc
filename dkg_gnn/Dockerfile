# Start from Merlin Pytorch v0.5.3 Container from NGC
FROM nvcr.io/nvidia/nvcr.io/ea-bignlp/ga-participants/nemofw-training:23.11
#tritonserver:23.10-trtllm-python-py3

WORKDIR /workspace
COPY FinDKG_LLM /workspace/FinDKG_LLM
Run git clone https://github.com/xiaohui-victor-li/FinDKG.git
#COPY CodeLlama-7b-Instruct codellama-7b-Instruct
#COPY CodeLlama-7b CodeLlama-7b
#COPY CodeLlama-13b codellama-13b
#COPY tensorrtllm_backend tensorrtllm_backend
#COPY TensorRT-LLM tensorrt_llm
#COPY model_analyzer /opt/tritonserver/model_analyzer
#COPY example_instructions.py example_instructions.py
#COPY example_infilling.py example_infilling.py
#COPY example_completion.py example_completion.py
#COPY llama-recipes llama-recipes
#COPY NeMo_Guardrails nemo_guardrails
#COPY transformer_engine transformer_engine
#COPY NeMo NeMo
RUN pip install jupyterlab
RUN pip install jupyterlab_nvdashboard
WORKDIR /workspace
#/opt/tritonserver
