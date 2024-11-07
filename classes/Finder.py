import torch
from sklearn.preprocessing import normalize

class Finder():
    def __init__(self, df, embeddings_matrix, model, transformador, tuned_matrix):
        self.df = df
        self.embeddings_matrix = embeddings_matrix
        self.tuned_matrix = tuned_matrix
        self.model = model
        self.transformador = transformador

    def predict_query(self, query, tuned=True):
        query_processed = self.model.encode([query])

        if tuned:
            query_processed = self.transformador(torch.tensor(query_processed))[1].detach().numpy()
            embeddings_matrix_ = normalize(self.tuned_matrix)
        else:
            embeddings_matrix_ = normalize(self.embeddings_matrix)

        query_processed_ = normalize(query_processed.reshape(1, -1))

        print(query_processed_.shape)
        print(embeddings_matrix_.shape)

        
        R = embeddings_matrix_ @ query_processed_.T

        df_ = self.df.copy()
        relevance = R.flatten()
        df_["relevance"] = relevance

        df_filtered = df_[relevance > 0.7]
        df_final = df_filtered.sort_values("relevance", ascending=False)

        # Selecionar colunas de interesse
        df_final = df_final[['title', 'abstract', 'relevance']]

        # print the top 10 abstracts
        tam = min(10, len(df_final))
        for i in range(tam):
            print(df_final['abstract'].iloc[i])
            print('-----------------------------------')
            
        return df_final.head(10)


