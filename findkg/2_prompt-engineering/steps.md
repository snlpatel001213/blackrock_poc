## Install required packages

```bash
pip install transformers torch
pip install -U "huggingface_hub[cli]"
pip install accelerate
huggingface-cli login 
```

use `extract_triplet.py` which used nvidia ngc deployed model for the triplet extraction
use `add_date_to_output.py` to add date to the output from origianl articles 