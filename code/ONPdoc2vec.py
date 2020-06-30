# -*- coding: utf-8 -*-
"""
ONPdoc2vec.py

doc2vec model for Online News Popularity prediction

Used for getting additional features using keywords, NER text etc

Send the input as ndarray, each row containing string separated by commas
model takes care of splitting the string to make words array as needed by gensim doc2vec

Model considers only the rows with valid values (Not None and Not Empty)

@author: vnithiya
"""

import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import pickle

from gensim.models.doc2vec import Doc2Vec, TaggedDocument

class ONPd2v():
    def __init__(self, train_data, size=50, pca_count=10):
        if not isinstance( train_data, np.ndarray):
            raise TypeError("Send input as numpy.ndarray") 
        
        self.train_data = train_data
        self.size = size
        self.pca_count = pca_count
        self.d2v_model = None
        self.pca = None
        self.scaler = None
        self.__train_model()
        
    def train(self, train_data, size=50, pca_count=10):
        if not isinstance( train_data, np.ndarray):
            raise TypeError("Send input as numpy.ndarray") 
            
        self.train_data = train_data
        self.size = size
        self.pca_count = pca_count
        self.d2v_model = None
        self.pca = None
        self.scaler = None
        self.__train_model()
        
    def infer_vector( self, doc_words):
        if self.d2v_model is None:
            raise ValueError("Model is not yet trained, train first and then call infer_vector")
        
        words_to_use = ''
        
        if isinstance( doc_words, str) and len( doc_words) > 0:
            words_to_use = doc_words
        else:
            words_to_use = 'empty'
        
        return self.d2v_model.infer_vector( words_to_use.split(","))
    
    # Save the model
    def save_model( self, filename):
        if self.d2v_model is None:
            raise ValueError("Model is not yet trained, train first and then call save_model")
        
        pickle.dump(self, open(filename, 'wb'))
    
    def infer_vector_pca( self, doc_words):
        if self.d2v_model is None:
            raise ValueError("Model is not yet trained, train first and then call infer_vector")
            
        words_to_use = ''
        
        if isinstance( doc_words, str) and len( doc_words) > 0:
            words_to_use = doc_words
        else:
            words_to_use = 'empty'
            
        inteferred_vector = self.d2v_model.infer_vector( words_to_use.split(","))
        
        # contains only one sample and hence reshaping
        inteferred_vector = inteferred_vector.reshape( 1, -1)
            
        scaled_vector = self.scaler.transform( inteferred_vector)
        
        return self.pca.transform( scaled_vector)[0]
    
    # Private method to train the model
    def __train_model(self):
        train_words_list = []
        doc_index = 0
        for value in self.train_data:
            if (not isinstance( value, str)) or (value is None) or len( value) == 0:
                # The row cannot be processed, ignore
                pass
            else:
                train_words_list.append( TaggedDocument( value.split(","), [doc_index] ) )
                doc_index += 1
                
        print( "Number of valid training row entries : " + str(len(train_words_list)) )
        
        self.d2v_model = Doc2Vec( train_words_list, vector_size=self.size,  window=2, min_count=1, dm=1)
        
        print( "Doc2vec model creation completed")
        
        # fitting PCA
        X = self.d2v_model[ self.d2v_model.wv.vocab]
        self.scaler = StandardScaler()
        self.scaler.fit(X)
        X_all = self.scaler.transform( X)
        
        self.pca = PCA( n_components=self.pca_count)
        self.pca.fit(X_all)

        print( "PCA fitting completed with n_components = " + str(self.pca_count))
  