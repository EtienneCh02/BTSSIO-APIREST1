Environnement avec journalisation et clé d'authentification de l'application
Utilisateur authentifié par SQL Serveur au travers de l'API Rest

Dépendances : 
pip install python-jose
pip install python-multipart
pip uninstall bcrypt passlib -y
pip install passlib[bcrypt] --no-cache-dir

Comment chiffrer un mot de passe : 
python -c "from passlib.context import CryptContext; pwd_context = CryptContext(schemes=['sha256_crypt'], deprecated='auto'); print(pwd_context.hash('password123'))"
