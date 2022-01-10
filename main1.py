import os
import pandas as pd
import numpy as np
import transformers
import numpy
import string
import flask
import torch

top_k = 10

#Step 1) Load Model and Tokenizer

#def load_model(model_name):
from transformers import BertTokenizer, BertForMaskedLM
bert_tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
bert_model = BertForMaskedLM.from_pretrained('bert-base-uncased').eval()
    
#Step 2) Add mask at the end since we want to perdict the next word.
    #The BERT requires this type of input to preprocess it
def get_prediction_eos(input_text):
    try:
        input_text += ' <mask>'#mask token for BERT input 
        res = get_all_predictions(input_text, top_clean=int(top_k))
        return res
    except Exception as error:
        pass
    
    
#Step 3) Encode and Decode
#add_special_tokens=True will add token for out of vocab words.
#tokenizer will take care of tokenizing the text.
def encode(tokenizer, text_sentence, add_special_tokens=True):
    text_sentence = text_sentence.replace('<mask>', tokenizer.mask_token)
    if tokenizer.mask_token == text_sentence.split()[-1]:
        text_sentence += ' .'## if <mask> is the last token, append a "." so that models dont predict punctuation.  
        input_ids = torch.tensor([tokenizer.encode(text_sentence, add_special_tokens=add_special_tokens)])#input ids tensor
        mask_idx = torch.where(input_ids == tokenizer.mask_token_id)[1].tolist()[0] #here we are getting ids for masked words
    return input_ids, mask_idx
    
    #In step 3 we got encoded inputs i.e tensors and now we will try to decode the tensors and find the words associated with those tensors.
    #step 4) we will decode the words and try to get words which are valid in the context of previous words.
    #https://www.geeksforgeeks.org/string-punctuation-in-python/
    #https://albertauyeung.github.io/2020/06/19/bert-tokenization.html#:~:text=Padding%20Token%20%5BPAD%5D,length%20of%20sentence%20as%20input.&text=For%20sentences%20that%20are%20shorter,represent%20paddings%20to%20the%20sentence.
def decode(tokenizer, pred_idx, top_clean):
    ignore_tokens = string.punctuation + '[PAD]'#this are the tokens which are to be ignored and not to be used.
    tokens = []#empty lsit of tokens
    for w in pred_idx:#loop to itrate input index.
        token = ''.join(tokenizer.decode(w).split())#this will decode the input id and save it in token variable.
        if token not in ignore_tokens:#this loop will check if the word belongs to the token which is to be ignored.
            tokens.append(token.replace('##', ''))#this will replace the ## tags if present in the words and will append the words into token list.
    return '\n'.join(tokens[:top_clean])#this will return top K words in the tokens list

#Step 4) Wrapper function for encoder and decoder
#this function will find the top k words.
def get_all_predictions(text_sentence, top_clean=5):
    input_ids, mask_idx = encode(bert_tokenizer, text_sentence)#we will convert input text to encode form i.e tensors.
    # since we will not do backward propogation we will not use gradient calculations.
    with torch.no_grad():#https://pytorch.org/docs/stable/generated/torch.no_grad.html 
        predict = bert_model(input_ids)[0]#we will pass all the input ids to bert model.
    bert = decode(bert_tokenizer, predict[0, mask_idx, :].topk(top_k).indices.tolist(), top_clean)#encoded words will now get converted back to words from 0th index to index of mask_ids.and this the magic where the contex will be captured as this is the pretrained BERT model and we will get sensible or meaninfull word at masked_ids place.
    return {'bert': bert}
# step 5) here we will use above function to encode the input text.
def get_prediction_eos(input_text):
    try:
        input_text += ' <mask>'#masked token is added to input text.
        results = get_all_predictions(input_text, top_clean=int(top_k))# here the function will do encoding decoding and produce the results.
        return results
    except Exception as error:
        pass

