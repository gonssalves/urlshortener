import hashlib
import json
import os

class URLStore:
    def __init__(self, storage_file='urls.json'):
        self.storage_file = storage_file
        self.urls = self._load_urls()
    
    def _load_urls(self):
        """Carrega URLs do arquivo de armazenamento"""
        if os.path.exists(self.storage_file):
            with open(self.storage_file, 'r') as f:
                return json.load(f)
        return {}
    
    def _save_urls(self):
        """Salva URLs no arquivo de armazenamento"""
        with open(self.storage_file, 'w') as f:
            json.dump(self.urls, f)
    
    def _generate_key(self, url):
        """Gera uma chave única para a URL"""
        # Usa SHA-256 e pega os primeiros 6 caracteres do hash
        hash_object = hashlib.sha256(url.encode())
        hex_dig = hash_object.hexdigest()
        return hex_dig[:6]
    
    def add_url(self, long_url):
        """Adiciona uma nova URL e retorna a chave"""
        # Verifica se a URL já existe
        for key, url in self.urls.items():
            if url == long_url:
                return key
        
        # Gera uma chave única
        key = self._generate_key(long_url)
        
        # Verifica colisões e gera nova chave se necessário
        counter = 1
        original_key = key
        while key in self.urls:
            if self.urls[key] == long_url:
                return key
            key = f"{original_key}_{counter}"
            counter += 1
        
        self.urls[key] = long_url
        self._save_urls()
        return key
    
    def get_url(self, key):
        """Obtém a URL original pela chave"""
        return self.urls.get(key)
    
    def delete_url(self, key):
        """Remove uma URL encurtada"""
        if key in self.urls:
            del self.urls[key]
            self._save_urls()
            return True
        return False