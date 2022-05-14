# UnrealAI

Application créée avec Unreal Engine dans le but d'expérimenter avec des AIs.

<div>
<img style="display: inline-block" src="https://cdn2.unrealengine.com/new-logo-share-1400x788-03-1400x788-c9d09f067a09.jpg" height="350">
<img style="display: inline-block" src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS7LiBjQVugSs8eyAwNPrgkYkcZDzMnLW1yyg&usqp=CAU" height="350">
</div>

# Comment installer le projet

## Versions
Ce projet nécéssite l'OS Windows ainsi que l'installation de Unreal Engine 4.25 et d'une version de Python 3.7+. 
Il est à noter que des packages avec des versions spécifiques seront installés sur la version de Python et donc une nouvelle version est recommandée.

## Installation
1. Cloner le projet via ce repo.
2. Compiler le projet est l'ouvrant avec Unreal Engine 4.25. Cette étape peut prendre un certain temps.
3. Installer les packages python en exécutant le fichier bat [InstallRequirements.bat](https://github.com/JustinACoder/H22-GR3-UnrealAI/tree/4.25/Plugins/machine-learning-remote-ue4/Server/ml-remote-server) dans le dossier du serveur. Cette étape peut notamment modifier les versions de tensorflow, de numpy et de bien d'autres packages dans la version de Python s'ils sont installés.
4. Dans Unreal Engine, *Launch* le projet, ce qui peut prendre quelques minutes, et *Cook Content for Windows* dans *File* en haut à gauche.

Le jeu est maintenant près à être joué.

# Jouer au jeux

Il existe deux manières de jouer: dans l'éditeur et avec le exe. 
Pour jouer dans l'éditeur, simplement appuyer sur le bouton *Play*.
Afin de jouer sur le exe, il faut tout d'abord activer le serveur avec le fichier [StartupServer.bat](https://github.com/JustinACoder/H22-GR3-UnrealAI/tree/4.25/Plugins/machine-learning-remote-ue4/Server/ml-remote-server) et ensuite le fichier exe située dans *Binairies/Win64/UnrealAI.exe* peut être exécuté. 

# Fonctionalités

Le projet est basé sur le plugin <a href="https://github.com/getnamo/tensorflow-ue4">tensorflow-ue4</a>

<h3>Datasets utilisés</h3>
<a href="https://github.com/googlecreativelab/quickdraw-dataset">Quick draw dataset</a><br>
<a href="https://www.kaggle.com/crawford/emnist?select=emnist-letters-test.csv">EMNIST</a>
