Real-time Popularity Prediction of Online News Articles 
=======================================================
by
Kannan Chandrasekaran (cs18mds11001), Sandeep Chopra(cs18mds11006), Venkatajalapathi Nithiyanandhan(cs18mds11029)

Given Dataset:
Mashable.com dataset with Id, URL, Shares and 17 features

Folder structure:
-----------------
From the project root,
/code    : contains all the notebook and python files
/data/input  : Contains the given dataset - OnlineNewsPopularity.xlsx 
/data/output : Contains all the data files generated in this project
/data/output/html   : HTML files of the given 7795 articles
/data/output/models : Trained Models of all the ML and NLP algorithms used in the project

Code structure:
---------------
We have divided our project in five areas as mentioned below: 
   Note: All the outputs (excel, model etc) mentioned for the notebooks will be available in respective folder under /data

0. Data Scrapping and Crawling
   0_Crawling.ipynb : 
       Crawls mashable.com to extract the HTML contents of input
       Creates SS_Extracted_content.xlsx
   0_Crawling_html_files.ipynb : 
       Crawls and stores the html files in data/output/html folder as individual files. 
       Needed this as earlier crawl, stored the html content in excel files where data was lost due to Excel's cell limit of 32kb size
   0_Recreate_Basic_Features.ipynb
       Recreates all 17 basic features from the HTML content
       Creates 0_recreated_basic_features.xlsx       
	   
1. Exploratory Data analysis
   1_Exploratory_Data_Analysis.ipynb
       Understanding Data Landscape, Data quality check, missing values, outlier and distribution analysis
	   
2. Feature Generation
   2_Day_of_Week_Extraction.ipynb
       Extracts day of the week features from the timestamp of publication
       Creates 2_Day_of_Week_Extraction.xlsx
	   
   2_NLP_Keyword extraction.ipynb
       Creates unique list of keywords extracted from HTML of every article
	   creates 2_keywords_list.xlsx
   
   2_Keywords Popularity-v2.ipynb
       Finding Popularity of the keywords and creates numerical features based on the keywords of an articles
	   creates 2_keywords_popularity_prediction.xlsx
	  
   2_NLP_Clustering.ipynb
       Unsupervised text clustering of news articles using TF-IDF and KMeans methods
	   creates 2_NLP_Clustering.xlsx
	   
   2_NLP_LDA_NMF_LSI-v2.ipynb
       Topic modelling using textual information (title and article content)
	   creates 2_NLP_LDA_NMF_LSI.xlsx
	   
   2_NLP_NER extraction.ipynb
        Extracts NER information from the article content
		creates SS_Extracted_content_NER_all.xlsx, SS_Extracted_content_NER_text.xlsx and 2_NER_Type_Count.xlsx

   2_NLP_Subjectivity_Polarity.ipynb
        Unsupervised text sentiment polarity and subjectivity using textblob
		creates 2_sentiment_polarity_subjectivity.xlsx
	
   ONPdoc2vec.py
        Reusable helper class to generate Doc2vec models and infer
		
   2_ONPdoc2vec_entire_content.ipynb
        Doc2vec based features extraction. Creates 100 dimensions and 10 PCA for each of the 4 components
		Uses ONPdoc2vec.py
		Creates 2_d2v_content.xlsx, 2_d2v_keywords.xlsx, 2_d2v_NER_list.xlsx, 2_d2v_NER_most_common.xlsx
		Also creates the models d2v_content.model, d2v_keywords.model, d2v_NER_list.model and 2_d2v_NER_most_common.model
		   
3. Model building, model Training and Benchmarking
   3_Benchmarking_Regression_and_DL_IIT_Outlier_Scale-95thPercentileIQR-Scale-V1.ipynb
        Benchmarking of traditional ML and Deep learning algorithm based models
        Trains and Dumps all the model files (as pickle files) to be used for by realtime prediction pipeline

   3_DL_Tuning_Grid_Search.ipynb
        Deep Learning model hyperparameters tuning
   
4. Real time prediction for any URL (in given set or new unseen URL)
   4_Demo_Pipeline-v6.ipynb
        End to End pipeline notebook
		For the given URL, scraps the HTML content, creates the features, standarizes them using trained standard scalers
		Uses all the models created during training time and predicts the popularity of the given URL
		Outputs the prediction based on ensemble of 3 best performing models (ElasticNet, Gradient Boosting and XGBoost)
		
		