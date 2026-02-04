Environnement avec journalisation et clé d'authentification de l'application
Utilisateur authentifié par SQL Serveur au travers de l'API Rest + QR Code avec clé stockée sur SQL au travers de l'API

Dépendances : 
pip install python-jose
pip install python-multipart
pip uninstall bcrypt passlib -y
pip install passlib[bcrypt] --no-cache-dir
pip install pillow


Comment chiffrer un mot de passe : 
python -c "from passlib.context import CryptContext; pwd_context = CryptContext(schemes=['sha256_crypt'], deprecated='auto'); print(pwd_context.hash('password123'))"
