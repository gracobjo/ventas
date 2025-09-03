"""
🎯 Sistema de Recomendaciones Híbrido
Combina collaborative filtering y content-based filtering
"""

import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.sparse import csr_matrix
import implicit
import warnings
import joblib
import os

warnings.filterwarnings('ignore')

class RecommendationSystem:
    """Sistema de recomendaciones híbrido"""
    
    def __init__(self):
        self.user_item_matrix = None
        self.product_similarity = None
        self.user_similarity = None
        self.collaborative_model = None
        self.content_model = None
        self.hybrid_weights = {'collaborative': 0.6, 'content': 0.4}
        self.models_dir = "app/models"
        
        # Crear directorio de modelos si no existe
        os.makedirs(self.models_dir, exist_ok=True)
    
    def create_user_item_matrix(self, df_spark):
        """Crea matriz usuario-producto desde Spark DataFrame"""
        print("📊 Creando matriz usuario-producto...")
        
        # Convertir a pandas para facilitar el procesamiento
        df_pandas = df_spark.toPandas()
        
        # Crear rating implícito basado en cantidad y frecuencia
        df_pandas['rating_implicito'] = np.log1p(df_pandas['cantidad']) * \
                                       (1 + df_pandas['total'] / 1000)
        
        # Matriz usuario-producto
        self.user_item_matrix = df_pandas.pivot_table(
            index='customer_id',
            columns='product_id',
            values='rating_implicito',
            fill_value=0
        )
        
        print(f"✅ Matriz creada: {self.user_item_matrix.shape}")
        return self.user_item_matrix
    
    def train_collaborative_filtering(self):
        """Entrena modelo de collaborative filtering"""
        print("🤝 Entrenando collaborative filtering...")
        
        # Convertir matriz a formato CSR para implicit
        matrix_csr = csr_matrix(self.user_item_matrix.values)
        
        # Modelo ALS (Alternating Least Squares)
        self.collaborative_model = implicit.als.AlternatingLeastSquares(
            factors=50,
            regularization=0.01,
            iterations=50,
            random_state=42
        )
        
        # Entrenar modelo
        self.collaborative_model.fit(matrix_csr.T)
        
        print("✅ Collaborative filtering entrenado")
        return self.collaborative_model
    
    def train_content_based_filtering(self, productos_df):
        """Entrena modelo content-based"""
        print("📝 Entrenando content-based filtering...")
        
        # Convertir Spark DataFrame a pandas
        productos_pandas = productos_df.toPandas()
        
        # Crear características de texto combinando nombre y categoría
        productos_pandas['texto_combinado'] = productos_pandas['nombre'] + ' ' + \
                                             productos_pandas['categoria']
        
        # Vectorización TF-IDF
        tfidf = TfidfVectorizer(
            max_features=1000,
            stop_words='english',
            ngram_range=(1, 2)
        )
        
        tfidf_matrix = tfidf.fit_transform(productos_pandas['texto_combinado'])
        
        # Calcular similitud coseno entre productos
        self.product_similarity = cosine_similarity(tfidf_matrix)
        
        # Guardar vectorizador
        self.content_model = {
            'tfidf': tfidf,
            'product_ids': productos_pandas['product_id'].values,
            'similarity_matrix': self.product_similarity
        }
        
        print("✅ Content-based filtering entrenado")
        return self.content_model
    
    def train_hybrid_model(self, df_spark, productos_df):
        """Entrena modelo híbrido combinando ambos enfoques"""
        print("🔄 Entrenando modelo híbrido...")
        
        # Crear matriz usuario-producto
        self.create_user_item_matrix(df_spark)
        
        # Entrenar collaborative filtering
        self.train_collaborative_filtering()
        
        # Entrenar content-based filtering
        self.train_content_based_filtering(productos_df)
        
        print("✅ Modelo híbrido entrenado")
    
    def get_collaborative_recommendations(self, customer_id, n_recommendations=5):
        """Obtiene recomendaciones usando collaborative filtering"""
        if customer_id not in self.user_item_matrix.index:
            return [], "Cliente no encontrado"
        
        # Obtener índice del usuario
        user_idx = self.user_item_matrix.index.get_loc(customer_id)
        
        # Predicciones del modelo ALS
        recommendations = self.collaborative_model.recommend(
            user_idx, 
            self.user_item_matrix.values, 
            N=n_recommendations
        )
        
        # Convertir a formato legible
        results = []
        for product_idx, score in recommendations:
            product_id = self.user_item_matrix.columns[product_idx]
            results.append((product_id, score))
        
        return results, "Éxito"
    
    def get_content_based_recommendations(self, customer_id, n_recommendations=5):
        """Obtiene recomendaciones usando content-based filtering"""
        if customer_id not in self.user_item_matrix.index:
            return [], "Cliente no encontrado"
        
        # Obtener productos que el usuario ya compró
        user_ratings = self.user_item_matrix.loc[customer_id]
        purchased_products = user_ratings[user_ratings > 0].index.tolist()
        
        if not purchased_products:
            return [], "Usuario sin historial de compras"
        
        # Calcular similitud promedio con productos comprados
        product_scores = {}
        
        for product_id in self.content_model['product_ids']:
            if product_id in purchased_products:
                continue
            
            # Obtener índice del producto
            product_idx = np.where(self.content_model['product_ids'] == product_id)[0][0]
            
            # Calcular similitud con productos comprados
            similarities = []
            for purchased_product in purchased_products:
                purchased_idx = np.where(self.content_model['product_ids'] == purchased_product)[0][0]
                similarity = self.content_model['similarity_matrix'][product_idx][purchased_idx]
                similarities.append(similarity)
            
            # Score promedio
            if similarities:
                product_scores[product_id] = np.mean(similarities)
        
        # Ordenar y obtener top N
        recommendations = sorted(
            product_scores.items(), 
            key=lambda x: x[1], 
            reverse=True
        )[:n_recommendations]
        
        return recommendations, "Éxito"
    
    def get_hybrid_recommendations(self, customer_id, n_recommendations=5):
        """Obtiene recomendaciones híbridas combinando ambos enfoques"""
        print(f"🎯 Generando recomendaciones híbridas para {customer_id}...")
        
        # Obtener recomendaciones de ambos modelos
        collab_recs, collab_status = self.get_collaborative_recommendations(
            customer_id, n_recommendations * 2
        )
        content_recs, content_status = self.get_content_based_recommendations(
            customer_id, n_recommendations * 2
        )
        
        if collab_status != "Éxito" and content_status != "Éxito":
            return [], "No se pudieron generar recomendaciones"
        
        # Combinar scores
        hybrid_scores = {}
        
        # Agregar scores collaborative
        for product_id, score in collab_recs:
            if product_id not in hybrid_scores:
                hybrid_scores[product_id] = {'collaborative': 0, 'content': 0}
            hybrid_scores[product_id]['collaborative'] = score
        
        # Agregar scores content-based
        for product_id, score in content_recs:
            if product_id not in hybrid_scores:
                hybrid_scores[product_id] = {'collaborative': 0, 'content': 0}
            hybrid_scores[product_id]['content'] = score
        
        # Calcular score híbrido
        final_scores = {}
        for product_id, scores in hybrid_scores.items():
            hybrid_score = (
                scores['collaborative'] * self.hybrid_weights['collaborative'] +
                scores['content'] * self.hybrid_weights['content']
            )
            final_scores[product_id] = hybrid_score
        
        # Ordenar y obtener top N
        recommendations = sorted(
            final_scores.items(), 
            key=lambda x: x[1], 
            reverse=True
        )[:n_recommendations]
        
        return recommendations, "Éxito"
    
    def get_similar_products(self, product_id, n_similar=5):
        """Encuentra productos similares a uno dado"""
        if product_id not in self.content_model['product_ids']:
            return [], "Producto no encontrado"
        
        # Obtener índice del producto
        product_idx = np.where(self.content_model['product_ids'] == product_id)[0][0]
        
        # Obtener similitudes
        similarities = self.content_model['similarity_matrix'][product_idx]
        
        # Obtener índices de productos más similares (excluyendo el mismo producto)
        similar_indices = np.argsort(similarities)[::-1][1:n_similar+1]
        
        # Convertir a formato legible
        similar_products = []
        for idx in similar_indices:
            similar_product_id = self.content_model['product_ids'][idx]
            similarity_score = similarities[idx]
            similar_products.append((similar_product_id, similarity_score))
        
        return similar_products, "Éxito"
    
    def evaluate_recommendations(self, test_users=None, n_test=50):
        """Evalúa la calidad de las recomendaciones"""
        print("📊 Evaluando sistema de recomendaciones...")
        
        if test_users is None:
            # Seleccionar usuarios aleatorios para evaluación
            all_users = self.user_item_matrix.index.tolist()
            test_users = np.random.choice(all_users, min(n_test, len(all_users)), replace=False)
        
        results = {
            'collaborative': {'precision': [], 'recall': []},
            'content': {'precision': [], 'recall': []},
            'hybrid': {'precision': [], 'recall': []}
        }
        
        for user_id in test_users:
            # Obtener productos reales del usuario
            user_ratings = self.user_item_matrix.loc[user_id]
            real_products = set(user_ratings[user_ratings > 0].index)
            
            if len(real_products) < 2:
                continue
            
            # Dividir en train/test (leave-one-out)
            for test_product in real_products:
                # Simular que no conocemos este producto
                temp_ratings = user_ratings.copy()
                temp_ratings[test_product] = 0
                
                # Generar recomendaciones
                collab_recs, _ = self.get_collaborative_recommendations(user_id, 10)
                content_recs, _ = self.get_content_based_recommendations(user_id, 10)
                hybrid_recs, _ = self.get_hybrid_recommendations(user_id, 10)
                
                # Calcular métricas
                for model_name, recs in [('collaborative', collab_recs), 
                                       ('content', content_recs), 
                                       ('hybrid', hybrid_recs)]:
                    recommended_products = set([rec[0] for rec in recs])
                    
                    if len(recommended_products) > 0:
                        precision = len(recommended_products & {test_product}) / len(recommended_products)
                        recall = len(recommended_products & {test_product}) / 1
                        
                        results[model_name]['precision'].append(precision)
                        results[model_name]['recall'].append(recall)
        
        # Calcular métricas promedio
        evaluation = {}
        for model_name, metrics in results.items():
            if metrics['precision']:
                evaluation[model_name] = {
                    'precision': np.mean(metrics['precision']),
                    'recall': np.mean(metrics['recall']),
                    'f1_score': 2 * np.mean(metrics['precision']) * np.mean(metrics['recall']) / 
                               (np.mean(metrics['precision']) + np.mean(metrics['recall']))
                }
        
        print("✅ Evaluación completada")
        return evaluation
    
    def save_models(self):
        """Guarda los modelos entrenados"""
        print("💾 Guardando modelos de recomendaciones...")
        
        models_to_save = {
            'user_item_matrix': self.user_item_matrix,
            'collaborative_model': self.collaborative_model,
            'content_model': self.content_model,
            'hybrid_weights': self.hybrid_weights
        }
        
        for name, model in models_to_save.items():
            if model is not None:
                joblib.dump(model, f"{self.models_dir}/{name}.pkl")
        
        print("✅ Modelos guardados")
    
    def load_models(self):
        """Carga modelos guardados"""
        print("📂 Cargando modelos de recomendaciones...")
        
        try:
            self.user_item_matrix = joblib.load(f"{self.models_dir}/user_item_matrix.pkl")
            print("✅ Matriz usuario-producto cargada")
        except:
            print("⚠️ No se pudo cargar matriz usuario-producto")
        
        try:
            self.collaborative_model = joblib.load(f"{self.models_dir}/collaborative_model.pkl")
            print("✅ Modelo collaborative cargado")
        except:
            print("⚠️ No se pudo cargar modelo collaborative")
        
        try:
            self.content_model = joblib.load(f"{self.models_dir}/content_model.pkl")
            print("✅ Modelo content-based cargado")
        except:
            print("⚠️ No se pudo cargar modelo content-based")
        
        try:
            self.hybrid_weights = joblib.load(f"{self.models_dir}/hybrid_weights.pkl")
            print("✅ Pesos híbridos cargados")
        except:
            print("⚠️ No se pudieron cargar pesos híbridos")
    
    def get_system_stats(self):
        """Obtiene estadísticas del sistema de recomendaciones"""
        if self.user_item_matrix is None:
            return None
        
        stats = {
            'num_users': len(self.user_item_matrix.index),
            'num_products': len(self.user_item_matrix.columns),
            'matrix_density': (self.user_item_matrix > 0).sum().sum() / \
                            (self.user_item_matrix.shape[0] * self.user_item_matrix.shape[1]),
            'avg_ratings_per_user': (self.user_item_matrix > 0).sum(axis=1).mean(),
            'avg_ratings_per_product': (self.user_item_matrix > 0).sum(axis=0).mean()
        }
        
        return stats

