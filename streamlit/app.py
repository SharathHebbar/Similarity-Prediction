import streamlit as st
import torch
from transformers import AutoTokenizer, AutoModel
from sentence_transformers import util
class SentenceSimiliarity():

    def __init__(self, sentence1, sentence2):
        self.sentence1 = sentence1
        self.sentence2 = sentence2
        self.model_name = "bert-base-uncased"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModel.from_pretrained(self.model_name)

    def tokenize(self):
        tokenized1 = self.tokenizer(
            self.sentence1,
            return_tensors='pt',
            padding=True,
            truncation=True
        )
        tokenized2 = self.tokenizer(
            self.sentence2,
            return_tensors='pt',
            padding=True,
            truncation=True
        )
        return tokenized1, tokenized2

    def get_embeddings(self):
        tokenized1, tokenized2 = self.tokenize()
        with torch.no_grad():
            embeddings1 = self.model(**tokenized1).last_hidden_state.mean(dim=1)
            embeddings2 = self.model(**tokenized2).last_hidden_state.mean(dim=1)
        return embeddings1, embeddings2
    
    def get_similarity_scores(self):
        embeddings1, embeddings2 = self.get_embeddings()
        scores = util.cos_sim(embeddings1, embeddings2)
        return scores

    
    def results(self):
        scores = self.get_similarity_scores()
        statement = f"The sentence has {scores.item() * 100:.2f}% similarity"
        return statement
    

class UI():

    def __init__(self):
        st.title("Sentence Similiarity Checker")
        st.caption("You can use this for checking similarity between resume and job description")
    
    def get(self):
        self.sentence1 = st.text_area(
            label="Sentence 1",
            help="This is a parent text the next text will be compared with this text"
        )
        self.sentence2 = st.text_area(
            label="Sentence 2",
            help="This is a child text"
        )
        self.button = st.button(
            label="Check",
            help='Check Sentence Similarity'
        )

    def result(self):
        self.get()
        ss = SentenceSimiliarity(self.sentence1, self.sentence2)
        
        if self.button:
            st.text(ss.results())
        # print(ss.results())

ui = UI()
ui.result()
