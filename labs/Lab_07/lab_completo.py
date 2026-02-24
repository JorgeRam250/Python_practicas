#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LABORATORIO COMPLETO: HTTP y Consumo de APIs con Python
======================================================

Este archivo integra todos los conceptos del laboratorio en un solo proyecto práctico:
- Cliente HTTP robusto con reintentos y timeouts
- Descarga de múltiples archivos usando streaming
- API RESTful completa para gestionar usuarios y posts
- Manejo profesional de errores
- Logging y monitoreo

Autor: Programador Python Experto
Nivel: Completo
"""

import httpx
import json
import time
import logging
import sys
import io
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from utils.http_client import UniversalHTTPClient
from utils.exceptions import HTTPClientError, TimeoutError, RetryExhaustedError, DownloadError

# Configurar codificación para Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('lab_http.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class User:
    """Modelo de datos para usuarios"""
    id: int
    name: str
    email: str
    phone: str
    website: str

@dataclass
class Post:
    """Modelo de datos para posts"""
    id: int
    title: str
    body: str
    userId: int

class APILabManager:
    """
    Gestor principal del laboratorio que integra todas las funcionalidades
    """
    
    def __init__(self):
        """Inicializa el gestor con el cliente HTTP universal"""
        self.client = UniversalHTTPClient(
            timeout_connect=3.0,
            timeout_read=15.0,
            timeout_write=5.0,
            max_retries=3,
            retry_delay=1.0,
            chunk_size=16384
        )
        
        self.base_url = "https://jsonplaceholder.typicode.com"
        logger.info("🚀 APILabManager inicializado")
    
    def get_all_users(self) -> List[User]:
        """
        Obtiene todos los usuarios de la API
        """
        logger.info("👥 Obteniendo todos los usuarios...")
        
        try:
            response = self.client.get(f"{self.base_url}/users")
            users_data = response.json()
            
            users = []
            for user_data in users_data:
                user = User(
                    id=user_data['id'],
                    name=user_data['name'],
                    email=user_data['email'],
                    phone=user_data['phone'],
                    website=user_data['website']
                )
                users.append(user)
            
            logger.info(f"✅ {len(users)} usuarios obtenidos")
            return users
            
        except Exception as e:
            logger.error(f"❌ Error obteniendo usuarios: {e}")
            raise HTTPClientError(f"No se pudieron obtener los usuarios: {e}")
    
    def get_user_posts(self, user_id: int) -> List[Post]:
        """
        Obtiene todos los posts de un usuario específico
        """
        logger.info(f"📝 Obteniendo posts del usuario {user_id}...")
        
        try:
            response = self.client.get(f"{self.base_url}/posts", params={"userId": user_id})
            posts_data = response.json()
            
            posts = []
            for post_data in posts_data:
                post = Post(
                    id=post_data['id'],
                    title=post_data['title'],
                    body=post_data['body'],
                    userId=post_data['userId']
                )
                posts.append(post)
            
            logger.info(f"✅ {len(posts)} posts obtenidos del usuario {user_id}")
            return posts
            
        except Exception as e:
            logger.error(f"❌ Error obteniendo posts del usuario {user_id}: {e}")
            raise HTTPClientError(f"No se pudieron obtener los posts: {e}")
    
    def create_post(self, user_id: int, title: str, body: str) -> Post:
        """
        Crea un nuevo post para un usuario
        """
        logger.info(f"📤 Creando post para usuario {user_id}...")
        
        try:
            post_data = {
                "title": title,
                "body": body,
                "userId": user_id
            }
            
            response = self.client.post(f"{self.base_url}/posts", post_data)
            created_data = response.json()
            
            post = Post(
                id=created_data['id'],
                title=created_data['title'],
                body=created_data['body'],
                userId=created_data['userId']
            )
            
            logger.info(f"✅ Post creado con ID: {post.id}")
            return post
            
        except Exception as e:
            logger.error(f"❌ Error creando post: {e}")
            raise HTTPClientError(f"No se pudo crear el post: {e}")
    
    def download_user_avatars(self, users: List[User]) -> List[str]:
        """
        Descarga avatares de ejemplo para los usuarios usando streaming
        """
        logger.info("🖼️ Descargando avatares de usuarios...")
        
        downloaded_files = []
        
        for i, user in enumerate(users, 1):
            try:
                # Usar una API de avatares con el email del usuario
                avatar_url = f"https://api.dicebear.com/7.x/avataaars/svg?seed={user.email}"
                destination = f"downloads/avatars/{user.id}_{user.name.replace(' ', '_')}.svg"
                
                logger.info(f"📥 Descargando avatar {i}/{len(users)}: {user.name}")
                
                file_path = self.client.download_stream(avatar_url, destination)
                downloaded_files.append(file_path)
                
            except Exception as e:
                logger.warning(f"⚠️ No se pudo descargar avatar para {user.name}: {e}")
        
        logger.info(f"✅ {len(downloaded_files)} avatares descargados")
        return downloaded_files
    
    def generate_user_report(self, user_id: int) -> str:
        """
        Genera un reporte completo de un usuario con sus posts
        """
        logger.info(f"📊 Generando reporte para usuario {user_id}...")
        
        try:
            # Obtener información del usuario
            users = self.get_all_users()
            user = next((u for u in users if u.id == user_id), None)
            
            if not user:
                raise HTTPClientError(f"Usuario {user_id} no encontrado")
            
            # Obtener posts del usuario
            posts = self.get_user_posts(user_id)
            
            # Generar reporte
            report = f"""
╔══════════════════════════════════════════════════════════════╗
║                    REPORTE DE USUARIO                         ║
╠══════════════════════════════════════════════════════════════╣
║ ID: {user.id:<60} ║
║ Nombre: {user.name:<57} ║
║ Email: {user.email:<57} ║
║ Teléfono: {user.phone:<55} ║
║ Website: {user.website:<56} ║
╠══════════════════════════════════════════════════════════════╣
║                    POSTS DEL USUARIO                          ║
╠══════════════════════════════════════════════════════════════╣
"""
            
            for i, post in enumerate(posts, 1):
                report += f"║ Post {i}: {post.title[:50]:<50} ID:{post.id:<5} ║\n"
            
            report += f"""
╠══════════════════════════════════════════════════════════════╣
║ Total de posts: {len(posts):<52} ║
║ Generado: {time.strftime('%Y-%m-%d %H:%M:%S'):<44} ║
╚══════════════════════════════════════════════════════════════╝
"""
            
            # Guardar reporte
            report_path = f"reports/user_{user_id}_report.txt"
            Path("reports").mkdir(exist_ok=True)
            
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(report)
            
            logger.info(f"✅ Reporte guardado en: {report_path}")
            return report_path
            
        except Exception as e:
            logger.error(f"❌ Error generando reporte: {e}")
            raise HTTPClientError(f"No se pudo generar el reporte: {e}")
    
    def run_complete_lab(self):
        """
        Ejecuta el laboratorio completo demostrando todas las funcionalidades
        """
        logger.info("🎯 Iniciando laboratorio completo...")
        
        try:
            # 1. Obtener todos los usuarios
            print("\n" + "="*60)
            print("👥 PASO 1: Obtener todos los usuarios")
            print("="*60)
            users = self.get_all_users()
            
            for user in users[:3]:  # Mostrar primeros 3
                print(f"  👤 {user.name} ({user.email})")
            
            # 2. Obtener posts del primer usuario
            print("\n" + "="*60)
            print("📝 PASO 2: Obtener posts de un usuario")
            print("="*60)
            first_user = users[0]
            posts = self.get_user_posts(first_user.id)
            
            print(f"  Posts de {first_user.name}:")
            for post in posts[:3]:  # Mostrar primeros 3
                print(f"    📄 {post.title[:50]}...")
            
            # 3. Crear un nuevo post
            print("\n" + "="*60)
            print("📤 PASO 3: Crear un nuevo post")
            print("="*60)
            new_post = self.create_post(
                user_id=first_user.id,
                title="Mi post desde el laboratorio HTTP",
                body="Este post fue creado usando nuestro cliente HTTP robusto"
            )
            print(f"  ✅ Post creado con ID: {new_post.id}")
            
            # 4. Descargar avatares (primeros 5 usuarios)
            print("\n" + "="*60)
            print("🖼️ PASO 4: Descargar avatares")
            print("="*60)
            downloaded_avatars = self.download_user_avatars(users[:5])
            print(f"  ✅ {len(downloaded_avatars)} avatares descargados")
            
            # 5. Generar reporte
            print("\n" + "="*60)
            print("📊 PASO 5: Generar reporte de usuario")
            print("="*60)
            report_path = self.generate_user_report(first_user.id)
            print(f"  ✅ Reporte generado: {report_path}")
            
            # 6. Mostrar resumen
            print("\n" + "="*60)
            print("🎉 LABORATORIO COMPLETADO EXITOSAMENTE")
            print("="*60)
            print(f"  👥 Usuarios procesados: {len(users)}")
            print(f"  📝 Posts obtenidos: {len(posts)}")
            print(f"  📤 Posts creados: 1")
            print(f"  🖼️ Avatares descargados: {len(downloaded_avatars)}")
            print(f"  📊 Reportes generados: 1")
            print(f"  📁 Archivos de log: lab_http.log")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Error en el laboratorio: {e}")
            print(f"\n❌ El laboratorio falló: {e}")
            return False
        
        finally:
            self.client.close()
            logger.info("🔒 Cliente HTTP cerrado")

def main():
    """
    Función principal del laboratorio completo
    """
    print("🐍 LABORATORIO COMPLETO: HTTP y Consumo de APIs con Python")
    print("=" * 70)
    print("Este laboratorio integra todos los conceptos aprendidos:")
    print("✓ Cliente HTTP robusto con reintentos y timeouts")
    print("✓ Streaming de archivos con progreso")
    print("✓ Manejo profesional de errores")
    print("✓ Logging y monitoreo")
    print("✓ API RESTful completa")
    print()
    
    # Crear directorios necesarios
    Path("downloads").mkdir(exist_ok=True)
    Path("downloads/avatars").mkdir(exist_ok=True)
    Path("reports").mkdir(exist_ok=True)
    
    # Ejecutar el laboratorio
    lab_manager = APILabManager()
    success = lab_manager.run_complete_lab()
    
    if success:
        print("\n🎊 ¡Felicidades! Has completado el laboratorio con éxito.")
        print("📚 Revisa los archivos generados en las carpetas:")
        print("  📁 downloads/ - Avatares descargados")
        print("  📁 reports/ - Reportes generados")
        print("  📄 lab_http.log - Logs detallados")
    else:
        print("\n❌ El laboratorio no pudo completarse. Revisa los logs.")

if __name__ == "__main__":
    main()
