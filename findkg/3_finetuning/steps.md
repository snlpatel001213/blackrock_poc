Outside docker

docker run --gpus device=all --shm-size=20g --net=host --ulimit memlock=-1 --rm -it -v ${PWD}:/workspace -w /workspace -v ${PWD}/results:/rresults:/results nvcr.io/ea-bignlp/ga-participants/nemofw-training:23.08.03 bash

download llama 7b using /workspace/findkg/3_finetuning/3.1_download_llama7b.py

convert the model weight to .nemo format
python /opt/NeMo/scripts/nlp_language_modeling/convert_hf_llama_to_nemo.py --in-file=/workspace/findkg/3_finetuning/llama2-7b-hf --out-file=llama2-7b.nemo

# data processing
/workspace/findkg/3_finetuning/3.2_data_preprocessing.py 

# split data
/workspace/findkg/3_finetuning/3.3_data_split.py

SFT training 

MODEL="/workspace/findkg/3_finetuning/llama2-7b.nemo"
TRAIN="/workspace/data/processed/us-financial-news-articles/SFT_training/training.jsonl"
VALID="/workspace/data/processed/us-financial-news-articles/SFT_training/validation.jsonl"
TEST="/workspace/data/processed/us-financial-news-articles/SFT_training/test.jsonl"
VALID_NAMES="[/workspace/data/processed/us-financial-news-articles/SFT_training]"
CONCAT_SAMPLING_PROBS="[1.0]"
TP_SIZE=8
PP_SIZE=1

torchrun --nproc_per_node=8 /opt/NeMo/examples/nlp/language_modeling/tuning/megatron_gpt_sft.py /opt/NeMo/examples/nlp/language_modeling/tuning/megatron_gpt_sft.py    trainer.precision=bf16    trainer.devices=8    trainer.num_nodes=1    trainer.val_check_interval=0.1    trainer.max_steps=50    model.restore_from_path=${MODEL}    model.micro_batch_size=1    model.global_batch_size=128    model.tensor_model_parallel_size=${TP_SIZE}    model.pipeline_model_parallel_size=${PP_SIZE}    model.megatron_amp_O2=True    model.sequence_parallel=True    model.activations_checkpoint_granularity=selective    model.activations_checkpoint_method=uniform    model.optim.name=distributed_fused_adam    model.optim.lr=5e-6    model.answer_only_loss=True    model.data.train_ds.file_names=${TRAIN_DS}    model.data.validation_ds.file_names=${VALID_DS}    model.data.test_ds.file_names=${TEST_DS}    model.data.train_ds.concat_sampling_probabilities=${CONCAT_SAMPLING_PROBS}    model.data.train_ds.max_seq_length=2048    model.data.validation_ds.max_seq_length=2048    model.data.train_ds.micro_batch_size=1    model.data.train_ds.global_batch_size=128    model.data.validation_ds.micro_batch_size=1    model.data.validation_ds.global_batch_size=128    model.data.test_ds.micro_batch_size=1    model.data.test_ds.global_batch_size=256    model.data.train_ds.num_workers=0    model.data.validation_ds.num_workers=0    model.data.test_ds.num_workers=0    model.data.validation_ds.metric.name=loss    model.data.test_ds.metric.name=loss    exp_manager.create_wandb_logger=False    exp_manager.explicit_log_dir=/results    exp_manager.resume_if_exists=True    exp_manager.resume_ignore_no_checkpoint=True    exp_manager.create_checkpoint_callback=True    exp_manager.checkpoint_callback_params.monitor=validation_loss    exp_manager.checkpoint_callback_params.save_best_model=False    exp_manager.checkpoint_callback_params.save_nemo_on_train_end=True