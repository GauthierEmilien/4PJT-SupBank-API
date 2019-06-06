#!/bin/bash
echo "Installation de Python 3, MongoDB..."
sudo apt-get install -y python3 python3-tk python3-venv mongodb > /dev/null
echo "Creation de l'environnement virtuel..."
python3 -m venv ./venv
source ./venv/bin/activate
echo "Installation des packages XatomeCoin..."
pip install -r requirement.txt > /dev/null
echo "Installation terminee"
chmod +x ./Xatome.sh
echo "Pour lancer le projet, lancer la commande ./Xatome.sh"
