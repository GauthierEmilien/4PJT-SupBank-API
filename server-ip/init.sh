#!/bin/bash
echo "Installation de Python 3, MongoDB..."
sudo apt-get install python3 python3-venv mongodb > /dev/null
echo "Creation de l'environnement virtuel..."
python3 -m venv ./venv
source ./venv/bin/activate
echo "Installation des packages pour le serveur Xatome..."
pip install -r requirement.txt > /dev/null
echo "Installation terminee"
chmod +x ./Xatome-Server.sh
echo "Pour lancer le projet, lancer la commande ./Xatome-Server.sh"
