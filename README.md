# bert-chinese-ner


从[BERT-TF](https://github.com/google-research/bert)下载bert源代码，存放在路径下bert文件夹中

从[BERT-Base Chinese](https://storage.googleapis.com/bert_models/2018_11_03/chinese_L-12_H-768_A-12.zip)下载模型，存放在checkpoint文件夹下

使用BIO数据标注模式，使用自造的查询数据

最终实现对于查询中每个实体 (LOC, TIM, KPI) 分类出对应的标签

train：

```cmd
python BERT_NER.py --data_dir=data/ --bert_config_file=checkpoint/bert_config.json --init_checkpoint=checkpoint/bert_model.ckpt --vocab_file=vocab.txt --output_dir=./output/result_dir/
```

eval & predict:

```cmd
python BERT_NER.py --data_dir=data/ --bert_config_file=checkpoint/bert_config.json --init_checkpoint=checkpoint/bert_model.ckpt --vocab_file=vocab.txt --output_dir=./output/result_dir/ --do_train=False --do_eval=True --do_predict=True
```

## requirement



```python
python==3.8
tensorflow==1.15.0
scikit-learn
```

注意 BERT 支持的 tensorflow 版本和 python 版本

如果要更改标签种类, 需要在 `BERT_NER.py` 的 `get_labels()` 函数中更改标签名

然后在 `BERT_NER.py` 的 `383, 451, 452, 453` 行把常数 `149` 改成实际标签数加一 `num_labels + 1` (加一用于 padding)

