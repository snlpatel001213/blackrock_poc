## Install required packages

```bash
pip install transformers torch
pip install -U "huggingface_hub[cli]"
pip install accelerate
huggingface-cli login 
```

use `llm_api.py` which used nvidia ngc deployed model for the triplet extraction