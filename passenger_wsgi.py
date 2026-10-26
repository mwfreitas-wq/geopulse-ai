import sys
import os

# Adiciona o diretório da aplicação ao sys.path
sys.path.insert(0, os.path.dirname(__file__))

# Importa a aplicação FastAPI do GeoPulse
from app.main import app
from a2wsgi import ASGIMiddleware

# O Passenger (cPanel da HostGator) espera um objeto chamado 'application' compatível com WSGI
application = ASGIMiddleware(app)
