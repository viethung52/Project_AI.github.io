import colorama
import pickle
import random
import time
from colorama import Fore, Style, Back
import json
import numpy as np
from tensorflow import keras
from sklearn.preprocessing import LabelEncoder
from tkinter import *
root = Tk()
colorama.init()


with open("data.json") as file:
    data = json.load(file)

 # load trained model
model = keras.models.load_model('chat_model')

    # load tokenizer object
with open('tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)

    # load label encoder object
with open('label_encoder.pickle', 'rb') as enc:
        lbl_encoder = pickle.load(enc)

    # parameters
max_len = 20
def chat():
        inp = e.get()
        send = "User:" + inp
        txt.insert(END, "\n"+send)
        e.delete(0,END)
        result = model.predict(keras.preprocessing.sequence.pad_sequences(tokenizer.texts_to_sequences([inp]),
                                                                          truncating='post', maxlen=max_len))
        txt.insert(END,"\n")
        tag = lbl_encoder.inverse_transform([np.argmax(result)])
        

        for i in data['intents']:
            if i['tag'] == tag:
                send = "ChatBot:"
                txt.insert(END, "\n"+send + np.random.choice(i['responses']))
        txt.insert(END,"\n---------------------------------------------------------")

txt = Text(root)
txt.grid(row=0, column=0, columnspan=2)
e = Entry(root, width=100)
send = Button(root, text="Send", command=chat).grid(row=1, column=1)
e.grid(row=1, column=0)
root.title("CHATBOT FOR THE ELDERLY")
root.mainloop()