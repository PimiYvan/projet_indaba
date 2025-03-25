import sys
import os

# Ajoutez le répertoire src au chemin Python
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from indaba import server
application = server
