# UnrealAI

Application créée avec Unreal Engine dans le but d'expérimenter avec des AIs.

<div>
<img style="display: inline-block" src="https://cdn2.unrealengine.com/new-logo-share-1400x788-03-1400x788-c9d09f067a09.jpg" height="350">
<img style="display: inline-block" src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS7LiBjQVugSs8eyAwNPrgkYkcZDzMnLW1yyg&usqp=CAU" height="350">
</div>

# Comment installer le projet

En terme de version et d'OS, uniquement Windows est supporté et Unreal Engine 4.23 ainsi que Python 3.6 sont nécessaire.
Bien faire attention que les variables d'environnement contiennent le path vers Python 3.6. 
Afin de généré les Binaries et pouvoir jouer au jeux:
- Avoir installé Visual Studio (pas Visual Studio Code)
- Ouvrir le projet dans Unreal Engine 4.23 et launch le projet dans le menu tout à droite.
- Encore dans Unreal Engine, Edit > Cook content for Windows.

Maintenant un dossier Binaries est apparu dans le projet avec à l'intérieur le jeu
dans le fichier UnrealAI.exe.

# Fonctionalités

Le projet est basé sur le plugin <a href="https://github.com/getnamo/tensorflow-ue4">tensorflow-ue4</a>

<h3>Datasets utilisés</h3>
<a href="https://github.com/googlecreativelab/quickdraw-dataset">Quick draw dataset</a><br>
<a href="https://www.kaggle.com/crawford/emnist?select=emnist-letters-test.csv">EMNIST</a>
