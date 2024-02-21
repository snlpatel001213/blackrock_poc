docker run --gpus all --network host -it --rm --shm-size=8g -p 8888:8888 -p 8889:8889 -p 8787:8787 -p 8887:8887 -p 6006:6006 -p 8892:8892 --ulimit memlock=-1 --ulimit stack=67108864 -v /raid/fsi-wip/bhall/workspace/:/workspace --device=/dev/snd nvcr.io/nvidia/dgl:23.11-py3 bash
#nvcr.io/nvidia/tritonserver:23.12-trtllm-python-py3 bash 
#nvcr.io/r2kuatviomfd/triton_trt_llm_bh:23.12 
#nvcr.io/nvidian/sae/dawilliams_tensorrt_llm:aug-release-v1
#nvcr.io/nvidia/pytorch:23.10-py3
#nvcr.io/r2kuatviomfd/internal-sandbox/nfw_trt_llm_bhall:23.11
