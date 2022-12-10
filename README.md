# Kubernetes-python-cli
Little kubernetes python cli

How to use : 

Pour utiliser l'application, deux choix s'offrent à vous, le prmier étant d'utiliser le script directement, pour cela il vous faudra avoir python3.8+ ainsi que les packages nommés dans le fichier requirements.txt, ensuite il vous suffira d'exécuter le script

Le second est d'exécuter le ficher client.exe dans le dossier dist, il lancera l'application directement sans que vous n'ayer besoin d'installer python et ses packages.

Une fois exécutée, l'application vous demandera l'url de l'api kubernetes (il s'agit dans mon cas de https://"ip-du-master-kube":6443)

Puis on vous demandera de donner le chemin d'un dossier contanant deux fichier, le certificat de votre utilisateur (au format .crt) ainsi que sa clé (au format .key), pour éviter de devoir entrer tout le chemin, vous pouvez glisser le dossier (son icone pas ce qu'il contient) directement dans l'application et le chemin se copiera tout seul.

ATTENTION : Votre utilisateur doit déjà avoir été créé au préalable dans votre configuration kubernetes. Aussi ses droits influenceront les résultats affichés par l'application ( par exemple ne pas utiliser un compte avec des droit en lecture pour appliquer une configuration, l'application vous dira que vous n'avez pas les droits)

Une fois que vous avez donné le dossier, l'application ce présentera comme ceci :

Veuillez choisir une option :
                        namespace en cours : default
1.Name Spaces                                                                                                                  
2.Deployment
3.Pods
4.Services
5.Autoscaling
6.Appliquer
7.Supprimer
8.Quitter

Pour entrer dans un menu, il vous suffit de taper, le numéro inscrit à coté du menu, son nom affiché, son nom en anglais ou son surnom (ex: ns pour namespaces), aussi les noms des menus ne sont pas soumis à la casse

Chaque menu de Name Spaces à Autoscaling se présentera sous la forme :

Veuillez choisir une option :
                        namespace en cours : default
1.Lister
2.Décrire
3.Supprimer
4.Revenir
5.Quitter



Lister/list/get affichera les resources demandées dans un format proche de ce qu'affiche un kubectl get
Décrire/decrire/describe affichera les resourcesdemandées comme les afficherait un kubectl describe
Supprimer/delete vous demandera le nom d'une resource pour la supprimer (ne rien donner pourrait supprimer toutes les resources de ce type et a donc été bloqué pour éviter les mauvaises surprises)
Revenir revient au menu précédent
Quitter ferme l'application

Un menu supplémentaire se trouve dans namespaces, il s'agit de Changer qui vous demandera le nom du nouveau namespace courant.

Certains menus vous demanderont si vous voulez donner le nom d'une resource afin d'en afficher qu'une, vous pourrez aussi ne rien écrire et seulement appuyer sur entrer pour afficher toutes les resources de ce type possible dans le namespace. Attebtion : les noms sont soumis à la casse


Le menus Appliquer/apply et Supprimer/delete vous demanderont le chemin d'un fichier (que vous pouver glisser directement dans l'interface) celui-ci appliquera le fichier (update ou création) ou le supprimera en fonction du menu choisit. Ces menu affichront un describe des vos resources.


Après chaque action, un retour sera envoyé pour revenir au menu précédent il vous suffit d'appuyer sur entrée. 
