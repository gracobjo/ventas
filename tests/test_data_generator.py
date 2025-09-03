"""
Tests para el generador de datos sintéticos
"""

import pytest
import pandas as pd
import os
import sys

# Agregar el directorio backend al path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend', 'app'))

from utils.data_generator import DataGenerator

class TestDataGenerator:
    """Tests para la clase DataGenerator"""
    
    def setup_method(self):
        """Configuración inicial para cada test"""
        self.data_generator = DataGenerator()
        self.test_data_dir = "test_data"
        
        # Crear directorio de test si no existe
        if not os.path.exists(self.test_data_dir):
            os.makedirs(self.test_data_dir)
    
    def teardown_method(self):
        """Limpieza después de cada test"""
        # Limpiar archivos de test
        test_files = [
            f"{self.test_data_dir}/test_products.parquet",
            f"{self.test_data_dir}/test_customers.parquet",
            f"{self.test_data_dir}/test_sales.parquet"
        ]
        
        for file_path in test_files:
            if os.path.exists(file_path):
                os.remove(file_path)
        
        # Remover directorio de test si está vacío
        if os.path.exists(self.test_data_dir) and not os.listdir(self.test_data_dir):
            os.rmdir(self.test_data_dir)
    
    def test_generar_productos(self):
        """Test para generar productos"""
        products_df = self.data_generator.generar_productos(100)
        
        assert isinstance(products_df, pd.DataFrame)
        assert len(products_df) == 100
        assert 'product_id' in products_df.columns
        assert 'name' in products_df.columns
        assert 'category' in products_df.columns
        assert 'price' in products_df.columns
        assert 'cost' in products_df.columns
    
    def test_generar_clientes(self):
        """Test para generar clientes"""
        customers_df = self.data_generator.generar_clientes(50)
        
        assert isinstance(customers_df, pd.DataFrame)
        assert len(customers_df) == 50
        assert 'customer_id' in customers_df.columns
        assert 'name' in customers_df.columns
        assert 'email' in customers_df.columns
        assert 'segment' in customers_df.columns
    
    def test_generar_ventas(self):
        """Test para generar ventas"""
        # Primero generar productos y clientes
        products_df = self.data_generator.generar_productos(10)
        customers_df = self.data_generator.generar_clientes(5)
        
        sales_df = self.data_generator.generar_ventas(100, products_df, customers_df)
        
        assert isinstance(sales_df, pd.DataFrame)
        assert len(sales_df) == 100
        assert 'sale_id' in sales_df.columns
        assert 'customer_id' in sales_df.columns
        assert 'product_id' in sales_df.columns
        assert 'quantity' in sales_df.columns
        assert 'unit_price' in sales_df.columns
        assert 'total_amount' in sales_df.columns
        assert 'date' in sales_df.columns
    
    def test_save_and_load_data(self):
        """Test para guardar y cargar datos"""
        # Generar datos de test
        products_df = self.data_generator.generar_productos(10)
        customers_df = self.data_generator.generar_clientes(5)
        sales_df = self.data_generator.generar_ventas(50, products_df, customers_df)
        
        # Guardar datos
        products_path = f"{self.test_data_dir}/test_products.parquet"
        customers_path = f"{self.test_data_dir}/test_customers.parquet"
        sales_path = f"{self.test_data_dir}/test_sales.parquet"
        
        products_df.to_parquet(products_path)
        customers_df.to_parquet(customers_path)
        sales_df.to_parquet(sales_path)
        
        # Verificar que los archivos existen
        assert os.path.exists(products_path)
        assert os.path.exists(customers_path)
        assert os.path.exists(sales_path)
        
        # Cargar datos
        loaded_products = pd.read_parquet(products_path)
        loaded_customers = pd.read_parquet(customers_path)
        loaded_sales = pd.read_parquet(sales_path)
        
        # Verificar que los datos cargados son iguales
        assert len(loaded_products) == len(products_df)
        assert len(loaded_customers) == len(customers_df)
        assert len(loaded_sales) == len(sales_df)
    
    def test_get_combined_data(self):
        """Test para obtener datos combinados"""
        # Generar datos
        products_df = self.data_generator.generar_productos(10)
        customers_df = self.data_generator.generar_clientes(5)
        sales_df = self.data_generator.generar_ventas(50, products_df, customers_df)
        
        # Obtener datos combinados
        combined_df = self.data_generator.get_combined_data(products_df, customers_df, sales_df)
        
        assert isinstance(combined_df, pd.DataFrame)
        assert len(combined_df) == 50  # Debe tener el mismo número de filas que sales
        assert 'product_name' in combined_df.columns
        assert 'customer_name' in combined_df.columns
        assert 'category' in combined_df.columns
        assert 'segment' in combined_df.columns
    
    def test_data_validation(self):
        """Test para validar la calidad de los datos generados"""
        products_df = self.data_generator.generar_productos(100)
        customers_df = self.data_generator.generar_clientes(50)
        sales_df = self.data_generator.generar_ventas(200, products_df, customers_df)
        
        # Validar productos
        assert products_df['price'].min() > 0
        assert products_df['cost'].min() > 0
        assert (products_df['price'] >= products_df['cost']).all()
        
        # Validar clientes
        assert customers_df['email'].str.contains('@').all()
        assert len(customers_df['segment'].unique()) > 0
        
        # Validar ventas
        assert sales_df['quantity'].min() > 0
        assert sales_df['unit_price'].min() > 0
        assert sales_df['total_amount'].min() > 0
        assert (sales_df['total_amount'] == sales_df['quantity'] * sales_df['unit_price']).all()

if __name__ == "__main__":
    pytest.main([__file__])

