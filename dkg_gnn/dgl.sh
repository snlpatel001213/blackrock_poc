docker run --gpus all --network host -it --rm --shm-size=8g -p 8888:8888 -p 8889:8889 -p 8787:8787 -p 8887:8887 -p 6006:6006 -p 8892:8892 --ulimit memlock=-1 --ulimit stack=67108864 --device=/dev/snd nvcr.io/nvidia/dgl:23.11-py3 bash

