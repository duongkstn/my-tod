from CocCocTokenizer import PyTokenizer
import pandas as pd
T = PyTokenizer(load_nontone_data=True)
df = pd.read_excel("/media/user/Data/ToD-BERT/TODBERT_dialog_datasets/dialog_datasets/Translated/train_dumpdata_tod_taskmaster_translated.xlsx",
                   dtype=str)
df['trans_tokenized'] = df['trans'].apply(lambda x: " ".join(T.word_tokenize(x, tokenize_option=0)))

df[['text', 'trans_tokenized']].to_excel("/media/user/Data/ToD-BERT/TODBERT_dialog_datasets/dialog_datasets/Translated/train_dumpdata_tod_taskmaster_translated_tokenized.xlsx", index=False)