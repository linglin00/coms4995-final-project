python train_mask_gan.py \
  --data_dir='/home/ll2948/musicGan/ptb' \
  --batch_size=100 \
  --sequence_length=5 \
  --base_directory='/home/ll2948/musicGan/log' \
  --mask_strategy=random \
  --maskgan_ckpt='/home/ll2948/musicGan/log/train/model.ckpt-1080749' \
  --hparams="gen_rnn_size=32,dis_rnn_size=32,gen_num_layers=2,dis_num_layers=2,gen_learning_rate=0.000038877,gen_learning_rate_decay=1.0,gen_full_learning_rate_steps=2000000,gen_vd_keep_prob=0.33971,rl_discount_rate=0.89072,dis_learning_rate=5e-4,baseline_decay=0.99,dis_train_iterations=2,dis_pretrain_learning_rate=0.005,critic_learning_rate=5.1761e-7,dis_vd_keep_prob=0.71940" \
  --mode='TEST' \
  --max_steps=1000 \
  --generator_model='seq2seq_vd' \
  --discriminator_model='seq2seq_vd' \
  --is_present_rate=0.75 \
  --summaries_every=250 \
  --print_every=250 \
  --max_num_to_print=100 \
  --gen_training_strategy='reinforce' \
  --seq2seq_share_embedding=true \
  --baseline_method=critic \
  --attention_option=luong > test.log 2>&1 &
