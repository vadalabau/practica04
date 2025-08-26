"""
Módulo de base de datos para el Sistema de Gestión de Satélites
Implementa persistencia con SQLite y serialización JSON
"""

import sqlite3
import json
from typing import List, Dict, Any, Optional
from datetime import datetime
import os
from models import Satelite, Mision, DatosRecolectados, Sensor

class SatelliteDatabase:
    """Clase para manejar la base de datos de satélites"""
    
    def __init__(self, db_path: str = "../database/satellites.db"):
        self.db_path = db_path
        self.ensure_database_directory()
        self.init_database()
    
    def ensure_database_directory(self):
        """Asegura que el directorio de la base de datos existe"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
    
    def get_connection(self):
        """Obtiene una conexión a la base de datos"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Permite acceso por nombre de columna
        return conn
    
    def init_database(self):
        """Inicializa las tablas de la base de datos"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Tabla de satélites
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS satelites (
                id TEXT PRIMARY KEY,
                nombre TEXT NOT NULL,
                tipo TEXT NOT NULL,
                fecha_lanzamiento TEXT NOT NULL,
                orbita TEXT NOT NULL,
                estado TEXT NOT NULL,
                sensores_json TEXT
            )
        ''')
        
        # Tabla de misiones
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS misiones (
                id TEXT PRIMARY KEY,
                satelite_id TEXT NOT NULL,
                objetivo TEXT NOT NULL,
                zona_observacion TEXT NOT NULL,
                duracion TEXT NOT NULL,
                estado TEXT NOT NULL,
                fecha_creacion TEXT NOT NULL,
                FOREIGN KEY (satelite_id) REFERENCES satelites (id)
            )
        ''')
        
        # Tabla de datos recolectados
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS datos_recolectados (
                id TEXT PRIMARY KEY,
                satelite_id TEXT NOT NULL,
                tipo TEXT NOT NULL,
                datos TEXT NOT NULL,
                fecha TEXT NOT NULL,
                FOREIGN KEY (satelite_id) REFERENCES satelites (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    # Métodos para Satélites
    def guardar_satelite(self, satelite: Satelite) -> bool:
        """Guarda un satélite en la base de datos"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Serializar sensores a JSON
            sensores_json = json.dumps([sensor.to_dict() for sensor in satelite.sensores])
            
            cursor.execute('''
                INSERT OR REPLACE INTO satelites 
                (id, nombre, tipo, fecha_lanzamiento, orbita, estado, sensores_json)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                satelite.id, satelite.nombre, satelite.tipo, 
                satelite.fecha_lanzamiento, satelite.orbita, 
                satelite.estado, sensores_json
            ))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error guardando satélite: {e}")
            return False
    
    def obtener_satelite(self, satelite_id: str) -> Optional[Satelite]:
        """Obtiene un satélite por ID"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM satelites WHERE id = ?', (satelite_id,))
            row = cursor.fetchone()
            
            if row:
                # Deserializar sensores desde JSON
                sensores_data = json.loads(row['sensores_json']) if row['sensores_json'] else []
                sensores = [Sensor.from_dict(sensor_data) for sensor_data in sensores_data]
                
                satelite = Satelite(
                    nombre=row['nombre'],
                    tipo=row['tipo'],
                    fecha_lanzamiento=row['fecha_lanzamiento'],
                    orbita=row['orbita'],
                    estado=row['estado'],
                    sensores=sensores
                )
                satelite.id = row['id']
                
                conn.close()
                return satelite
            
            conn.close()
            return None
        except Exception as e:
            print(f"Error obteniendo satélite: {e}")
            return None
    
    def listar_satelites(self, filtros: Dict[str, Any] = None) -> List[Satelite]:
        """Lista todos los satélites con filtros opcionales"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            query = 'SELECT * FROM satelites'
            params = []
            
            if filtros:
                conditions = []
                if 'tipo' in filtros:
                    conditions.append('tipo = ?')
                    params.append(filtros['tipo'])
                if 'estado' in filtros:
                    conditions.append('estado = ?')
                    params.append(filtros['estado'])
                
                if conditions:
                    query += ' WHERE ' + ' AND '.join(conditions)
            
            cursor.execute(query, params)
            rows = cursor.fetchall()
            
            satelites = []
            for row in rows:
                # Deserializar sensores desde JSON
                sensores_data = json.loads(row['sensores_json']) if row['sensores_json'] else []
                sensores = [Sensor.from_dict(sensor_data) for sensor_data in sensores_data]
                
                satelite = Satelite(
                    nombre=row['nombre'],
                    tipo=row['tipo'],
                    fecha_lanzamiento=row['fecha_lanzamiento'],
                    orbita=row['orbita'],
                    estado=row['estado'],
                    sensores=sensores
                )
                satelite.id = row['id']
                satelites.append(satelite)
            
            conn.close()
            return satelites
        except Exception as e:
            print(f"Error listando satélites: {e}")
            return []
    
    # Métodos para Misiones
    def guardar_mision(self, mision: Mision) -> bool:
        """Guarda una misión en la base de datos"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR REPLACE INTO misiones 
                (id, satelite_id, objetivo, zona_observacion, duracion, estado, fecha_creacion)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                mision.id, mision.satelite_id, mision.objetivo,
                mision.zona_observacion, mision.duracion, 
                mision.estado, mision.fecha_creacion
            ))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error guardando misión: {e}")
            return False
    
    def obtener_mision(self, mision_id: str) -> Optional[Mision]:
        """Obtiene una misión por ID"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM misiones WHERE id = ?', (mision_id,))
            row = cursor.fetchone()
            
            if row:
                mision = Mision(
                    satelite_id=row['satelite_id'],
                    objetivo=row['objetivo'],
                    zona_observacion=row['zona_observacion'],
                    duracion=row['duracion'],
                    estado=row['estado']
                )
                mision.id = row['id']
                mision.fecha_creacion = row['fecha_creacion']
                
                conn.close()
                return mision
            
            conn.close()
            return None
        except Exception as e:
            print(f"Error obteniendo misión: {e}")
            return None
    
    def listar_misiones(self, filtros: Dict[str, Any] = None) -> List[Mision]:
        """Lista todas las misiones con filtros opcionales"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            query = 'SELECT * FROM misiones'
            params = []
            
            if filtros:
                conditions = []
                if 'satelite_id' in filtros:
                    conditions.append('satelite_id = ?')
                    params.append(filtros['satelite_id'])
                if 'estado' in filtros:
                    conditions.append('estado = ?')
                    params.append(filtros['estado'])
                
                if conditions:
                    query += ' WHERE ' + ' AND '.join(conditions)
            
            cursor.execute(query, params)
            rows = cursor.fetchall()
            
            misiones = []
            for row in rows:
                mision = Mision(
                    satelite_id=row['satelite_id'],
                    objetivo=row['objetivo'],
                    zona_observacion=row['zona_observacion'],
                    duracion=row['duracion'],
                    estado=row['estado']
                )
                mision.id = row['id']
                mision.fecha_creacion = row['fecha_creacion']
                misiones.append(mision)
            
            conn.close()
            return misiones
        except Exception as e:
            print(f"Error listando misiones: {e}")
            return []
    
    # Métodos para Datos Recolectados
    def guardar_datos_recolectados(self, datos: DatosRecolectados) -> bool:
        """Guarda datos recolectados en la base de datos"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR REPLACE INTO datos_recolectados 
                (id, satelite_id, tipo, datos, fecha)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                datos.id, datos.satelite_id, datos.tipo,
                datos.datos, datos.fecha
            ))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error guardando datos recolectados: {e}")
            return False
    
    def listar_datos_recolectados(self, filtros: Dict[str, Any] = None) -> List[DatosRecolectados]:
        """Lista todos los datos recolectados con filtros opcionales"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            query = 'SELECT * FROM datos_recolectados'
            params = []
            
            if filtros:
                conditions = []
                if 'satelite_id' in filtros:
                    conditions.append('satelite_id = ?')
                    params.append(filtros['satelite_id'])
                if 'tipo' in filtros:
                    conditions.append('tipo = ?')
                    params.append(filtros['tipo'])
                
                if conditions:
                    query += ' WHERE ' + ' AND '.join(conditions)
            
            query += ' ORDER BY fecha DESC'
            
            cursor.execute(query, params)
            rows = cursor.fetchall()
            
            datos_list = []
            for row in rows:
                datos = DatosRecolectados(
                    satelite_id=row['satelite_id'],
                    tipo=row['tipo'],
                    datos=row['datos']
                )
                datos.id = row['id']
                datos.fecha = row['fecha']
                datos_list.append(datos)
            
            conn.close()
            return datos_list
        except Exception as e:
            print(f"Error listando datos recolectados: {e}")
            return []
    
    def obtener_estadisticas(self) -> Dict[str, Any]:
        """Obtiene estadísticas del sistema"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Contar satélites por estado
            cursor.execute('SELECT estado, COUNT(*) as count FROM satelites GROUP BY estado')
            satelites_por_estado = dict(cursor.fetchall())
            
            # Contar misiones por estado
            cursor.execute('SELECT estado, COUNT(*) as count FROM misiones GROUP BY estado')
            misiones_por_estado = dict(cursor.fetchall())
            
            # Contar datos por tipo
            cursor.execute('SELECT tipo, COUNT(*) as count FROM datos_recolectados GROUP BY tipo')
            datos_por_tipo = dict(cursor.fetchall())
            
            # Total de registros
            cursor.execute('SELECT COUNT(*) FROM satelites')
            total_satelites = cursor.fetchone()[0]
            
            cursor.execute('SELECT COUNT(*) FROM misiones')
            total_misiones = cursor.fetchone()[0]
            
            cursor.execute('SELECT COUNT(*) FROM datos_recolectados')
            total_datos = cursor.fetchone()[0]
            
            conn.close()
            
            return {
                "total_satelites": total_satelites,
                "total_misiones": total_misiones,
                "total_datos": total_datos,
                "satelites_por_estado": satelites_por_estado,
                "misiones_por_estado": misiones_por_estado,
                "datos_por_tipo": datos_por_tipo
            }
        except Exception as e:
            print(f"Error obteniendo estadísticas: {e}")
            return {}
