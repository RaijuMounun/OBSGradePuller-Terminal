import keyring
import json
import os
from typing import List, Optional
from src.models import UserProfile

class AuthManager:
    SERVICE_ID = "OBS_Grade_Puller_App"
    
    # Dosya adı sabit, ama yolu dinamik olacak
    FILENAME = "profiles.json"

    def __init__(self):        
        if os.name == 'nt': # Windows
            base_path = os.getenv('LOCALAPPDATA')
        else: # Linux/Mac
            base_path = os.path.join(os.path.expanduser("~"), ".local", "share")

        # Klasör yolunu oluştur
        self.app_dir = os.path.join(base_path, "OBSGradePuller")
        
        # Klasör yoksa yarat (İlk çalışma)
        if not os.path.exists(self.app_dir):
            os.makedirs(self.app_dir)
            
        # Tam dosya yolu
        self.profile_path = os.path.join(self.app_dir, self.FILENAME)
        # -----------------------

        self._profiles = self._load_profiles()

    def _load_profiles(self) -> List[str]:
        """Kayıtlı kullanıcı adlarını JSON'dan yükler."""
        if not os.path.exists(self.profile_path):
            return []
        try:
            with open(self.profile_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []

    def _save_profiles(self):
        """Kullanıcı listesini JSON'a yazar."""
        with open(self.profile_path, "w", encoding="utf-8") as f:
            json.dump(self._profiles, f)

    def save_user(self, username: str, password: str):
        """Kullanıcıyı listeye ekler, şifreyi Keyring'e kilitler."""
        keyring.set_password(self.SERVICE_ID, username, password)
        
        if username not in self._profiles:
            self._profiles.append(username)
            self._save_profiles()

    def get_password(self, username: str) -> Optional[str]:
        return keyring.get_password(self.SERVICE_ID, username)

    def get_registered_users(self) -> List[str]:
        return self._profiles

    def delete_user(self, username: str):
        try:
            keyring.delete_password(self.SERVICE_ID, username)
        except:
            pass

        if username in self._profiles:
            self._profiles.remove(username)
            self._save_profiles()