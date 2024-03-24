from kashgari.corpus import ChineseDailyNerCorpus
from kashgari.tasks.labeling import BiLSTM_Model
from kashgari.embeddings import BERTEmbedding, BERTEmbeddingV2
import kashgari

kashgari.config.use_cudnn_cell = True
train_x, train_y = ChineseDailyNerCorpus.load_data('train')
test_x, test_y = ChineseDailyNerCorpus.load_data('test')
valid_x, valid_y = ChineseDailyNerCorpus.load_data('valid')

config_path = 'bert/albert_xlarge_zh_183k/albert_config_xlarge.json'
checkpoint_path = 'bert/albert_xlarge_zh_183k/albert_model.ckpt'
dict_path = 'bert/albert_xlarge_zh_183k/vocab.txt'

# embedding = BERTEmbeddingV2(dict_path, config_path, checkpoint_path,
#                                 bert_type='albert',
#                                 task=kashgari.CLASSIFICATION,
#                                 sequence_length=100)

# model = BiLSTM_Model()
# model.fit(train_x, train_y, valid_x, valid_y, epochs=5)


embedding = BERTEmbedding('bert/chinese_L-12_H-768_A-12',
                          task=kashgari.LABELING,
                          sequence_length=100)
model = BiLSTM_Model(embedding)
model.fit(train_x, train_y, valid_x, valid_y, epochs=5)
model.save('model/bilstm_ner')

query1 = [['不', '要', '朝', '北', '的', '房', '子']]
model = kashgari.utils.load_model('model/bilstm_ner')
res = model.predict_entities(query1)

def process_query(query):
    features = []
    lines_list = []
    for char in query:
        lines_list.append(char)
    features.append(lines_list)
    return features

query2 = '两房带电梯400万左右有吗？'
features = process_query(query2)
res = model.predict_entities(features)