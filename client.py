import json, requests, urllib3
from os import system
from os import listdir
from os import mkdir
import yaml
urllib3.disable_warnings()
clear = lambda : system('cls')

url = ""

currnamespace = "default"

headers = {"Content-type":"application/yaml",
           "Accept":"application/json"}

authuser = ("C:\\Users\\Tony\\Documents\\filetransfer\\myuser.crt","C:\\Users\\Tony\\Documents\\filetransfer\\myuser.key")
authadmin = ("C:\\Users\\Tony\\Documents\\filetransfer\\myadmin.crt","C:\\Users\\Tony\\Documents\\filetransfer\\myadmin.key")
auth = tuple()

def geturl():
    global url
    clear()
    saved_url = ""
    try: 
        with open("conf\\url.txt","r") as url_file:
            saved_url = url_file.readline()
    except:
        pass
    url = input(f"Veuillez entrer l'url de l'api (Laisser vide pour : {saved_url}) : ")
    if url == "":
        url = saved_url
    if url[-1] != "/":
        url+="/"
    try:
        with open("conf\\url.txt","w") as url_file:
            url_file.write(url)
            auth()
    except: 
        try:
            mkdir("conf")
            with open("conf\\url.txt","w") as url_file:
                url_file.write(url)
                auth()
        except Exception as e:
            input(e)
            geturl()
    return

def auth():
    global auth
    clear()
    path = input("Veuillez donner le chemin vers le certificat et sa clé (\"q\" pour quitter): ")
    if path == "q":
        return
    else:
        try:
            filenames = listdir(path)
            if len(filenames) != 2:
                input("Le nombre de fichiers dans le dossier n'est pas bon")
                auth()
            else:
                if "crt" in filenames[0]:
                    auth = (path+"\\"+filenames[0],path+"\\"+filenames[1])
                else:
                    auth = (path+"\\"+filenames[1],path+"\\"+filenames[0])
                menu()
        except Exception as e:
            input(e)
            auth()
    


def optionDisplay(options):
    clear()
    display = f"Veuillez choisir une option : \n\t\t\tnamespace en cours : {currnamespace}\n"
    x = 1
    for option in options:
        display+=f"{x}.{option}\n"
        x+=1
    display+="\n"
    return input(display)

def menu():
    global currnamespace
    choice = optionDisplay(("Name Spaces","Deployment","Pods","Services","Autoscaling","Appliquer","Supprimer","Quitter"))
    if choice.lower() in ("1","name spaces","namespaces","ns"):
        namespaces()
    elif choice.lower() in ("2","deployment","deploy"):
        deploy()
    elif choice.lower() in ("3","pods","pod","po"):
        pods()
    elif choice.lower() in ("4","services","svc"):
        services()
    elif choice.lower() in ("5","autoscaling","hpa"):
        hpa()
    elif choice.lower() in ("6","appliquer","apply"):
        apply()
    elif choice.lower() in ("7","supprimer","delete"):
        delete()
    elif choice.lower() in ("8","quitter"):
        return
    else:
        menu()
    return


def deploy():
    uri = f"apis/apps/v1/namespaces/{currnamespace}/deployments/"
    choice = optionDisplay(("Lister","Décrire","Supprimer","Revenir","Quitter"))
    if choice.lower() in ("1","lister","list","get"):
        name = input("Entrez le nom du déploiement (laisser vide pour tous) : ")
        clear()
        r = requests.get(url+uri+name,headers=headers,params={},cert=auth,verify=False).json()
        #pprint.pprint(r)
        try:
            test = r["code"]
            print(yaml.dump(r))
        except KeyError:    
            items = list()
            try:
                items = r["items"]
            except KeyError:
                items.append(r)
            if len(items) == 0:
                print("No resources of this type in this namespace")
            else:
                print("Name\t\tReady\tUp-to-date\tAvailable")
                for elem in items:
                    name = elem["metadata"]["name"]
                    curreplicas = ""
                    try:
                        curreplicas = str(elem["status"]["readyReplicas"])
                    except:
                        curreplicas = "0"
                    ready = curreplicas+"/"+str(elem["status"]["replicas"])
                    upto = elem["status"]["updatedReplicas"]
                    avail = ""
                    try:
                        avail = elem["status"]["availableReplicas"]
                    except:
                        avail = 0
                    print(f"{name}\t{ready}\t{upto}\t\t{avail}")
        input()
        deploy()
    elif choice.lower() in ("2","decrire","décrire","describe"):
        name = input("Entrez le nom du déploiement (laisser vide pour tous) : ")
        clear()
        print(yaml.dump(requests.get(url+uri+name,headers=headers,params={},cert=auth,verify=False).json()))
        input()
        deploy()
    elif choice.lower() in ("3","supprimer","delete"):
        name = input("Entrez le nom du déploiement (\"q\" pour quitter): ")
        name = name.replace(" ", "")
        if name != "q":
            if name != "":
                print(yaml.dump(requests.delete(url+uri+name,headers=headers,data={},cert=auth,verify=False).json()))
            else:
                print("Le nom ne peut pas être vide")
            input()
        deploy()
    elif choice.lower() in ("4","revenir"):
        menu()
    elif choice.lower() in ("5","quitter"):
        return
    else:
        deploy()
    return

def namespaces():
    uri="api/v1/namespaces/"
    choice = optionDisplay(("Lister","Décrire","Changer","Supprimer","Revenir","Quitter"))
    if choice.lower() in ("1","lister","list","get"):
        name = input("Entrez le nom du namespace (laisser vide pour tous) : ")
        clear()
        r = requests.get(url+uri+name,headers=headers,params={},cert=auth,verify=False).json()
        try:
            test = r["code"]
            print(yaml.dump(r))
        except KeyError:    
            items = list()
            try:
                items = r["items"]
            except KeyError:
                items.append(r)
            if len(items) == 0:
                print("No resources of this type in this namespace")
            else:
                print("Name")
                for elem in items:
                    name = elem["metadata"]["name"]
                    print(name)
            input()
        namespaces() 
    elif choice.lower() in ("2","decrire","décrire","describe"):
        name = input("Entrez le nom du namespace (laisser vide pour tous) : ")
        print(yaml.dump(requests.get(url+uri+name,headers=headers,params={},cert=auth,verify=False).json()))
        input()
        namespaces()  
    elif choice.lower() in ("3","changer"):
        global currnamespace
        currnamespace = input("Veuillez donner le nom du namespace : ")
        namespaces()
    elif choice.lower() in ("4","supprimer","delete"):
        name = input("Entrez le nom du namespace (\"q\" pour quitter): ")
        name = name.replace(" ", "")
        if name != "q":
            if dname != "":
                print(yaml.dump(requests.delete(url+uri+name,headers=headers,data={},cert=auth,verify=False).json()))
            else:
                print("Le nom ne peut pas être vide")
            input()
        namespaces()
    elif choice.lower() in ("5","revenir"):
        menu()
    elif choice.lower() in ("6","quitter"):
        return
    else:
        namespaces()
    return
    
def hpa():
    uri = f"apis/autoscaling/v2/namespaces/{currnamespace}/horizontalpodautoscalers/"
    choice = optionDisplay(("Lister","Décrire","Supprimer","Revenir","Quitter"))
    if choice.lower() in ("1","lister","list","get"):
        name = input("Entrez le nom de l'autoscaling (laisser vide pour tous) : ")
        clear()
        r = requests.get(url+uri+name,headers=headers,params={},cert=auth,verify=False).json()
        #pprint.pprint(r)
        try:
            test = r["code"]
            print(yaml.dump(r))
        except KeyError:    
            items = list()
            try:
                items = r["items"]
            except KeyError:
                items.append(r)
            if len(items) == 0:
                print("No resources of this type in this namespace")
            else:
                print("NAME\t\tREFERENCE\t\t\tTARGETS\tMINPODS\tMAXPODS\tREPLICAS")
                for elem in items:
                    name = elem["metadata"]["name"]
                    refspec = elem["spec"]["scaleTargetRef"]
                    ref = refspec["kind"]+"/"+refspec["name"]
                    targetcpu = elem["spec"]["metrics"][0]["resource"]["target"]["averageUtilization"]
                    currcpu = elem["status"]["currentMetrics"][0]["resource"]["current"]["averageUtilization"]
                    targets = f"{currcpu}%/{targetcpu}%"
                    minpod = elem["spec"]["minReplicas"]
                    maxpod = elem["spec"]["maxReplicas"]
                    replicas = elem["status"]["currentReplicas"]
                    print(f"{name}\t{ref}\t{targets}\t{minpod}\t{maxpod}\t{replicas}")
        input()
        hpa()
    elif choice.lower() in ("2","decrire","décrire","describe"):
        name = input("Entrez le nom de l'autoscaling (laisser vide pour tous) : ")
        clear()
        print(yaml.dump(requests.get(url+uri+name,headers=headers,params={},cert=auth,verify=False).json()))
        input()
        hpa()
    elif choice.lower() in ("3","supprimer","delete"):
        name = input("Entrez le nom d'autoscaling (\"q\" pour quitter): ")
        name = name.replace(" ", "")
        if name != "q":
            if dname != "":
                print(yaml.dump(requests.delete(url+uri+name,headers=headers,data={},cert=auth,verify=False).json()))
            else:
                print("Le nom ne peut pas être vide")
            input()
        hpa()
    elif choice.lower() in ("4","revenir"):
        menu()
    elif choice.lower() in ("5","quitter"):
        return
    else:
        hpa()
    return

def pods():
    uri=f"api/v1/namespaces/{currnamespace}/pods/"
    choice = optionDisplay(("Lister","Décrire","Supprimer","Revenir","Quitter"))
    if choice.lower() in ("1","lister","list","get"):
        name = input("Entrez le nom du pod (laisser vide pour tous) : ")
        clear()
        r = requests.get(url+uri+name,headers=headers,params={},cert=auth,verify=False).json()
        #pprint.pprint(r)
        try:
            test = r["code"]
            print(yaml.dump(r))
        except KeyError:    
            items = list()
            try:
                items = r["items"]
            except KeyError:
                items.append(r)
            if len(items) == 0:
                print("No resources of this type in this namespace")
            else:
                print("NAME\t\t\t\tREADY\tSTATUS\tRESTARTS\tIP")
                for elem in items:
                    name = elem["metadata"]["name"]
                    count = 0
                    restarts = 0
                    for container in elem['status']["containerStatuses"]:
                        if container["ready"] == True:
                            count += 1
                        if container["restartCount"] > restarts:
                            restarts = container["restartCount"]
                    ready = str(count)+"/"+str(len(elem['status']["containerStatuses"]))
                    status = elem["status"]["phase"]
                    ip = elem["status"]["podIP"]
                    print(f"{name}\t{ready}\t{status}\t{restarts}\t{ip}")
        input()
        pods()
    elif choice.lower() in ("2","decrire","décrire","describe"):
        name = input("Entrez le nom du pod (laisser vide pour tous) : ")
        clear()
        print(yaml.dump(requests.get(url+uri+name,headers=headers,params={},cert=auth,verify=False).json()))
        input()
        pods()
    elif choice.lower() in ("3","supprimer","delete"):
        name = input("Entrez le nom du pod (\"q\" pour quitter): ")
        name = name.replace(" ", "")
        if name != "q":
            if dname != "":
                print(yaml.dump(requests.delete(url+uri+name,headers=headers,data={},cert=auth,verify=False).json()))
            else:
                print("Le nom ne peut pas être vide")
            input()
        pods()
    elif choice.lower() in ("4","revenir"):
        menu()
    elif choice.lower() in ("5","quitter"):
        return
    else:
        pods
    return

def services():
    uri = f"api/v1/namespaces/{currnamespace}/services/"
    choice = optionDisplay(("Lister","Décrire","Supprimer","Revenir","Quitter"))
    if choice.lower() in ("1","lister","list","get"):
        name = input("Entrez le nom du service (laisser vide pour tous) : ")
        clear()
        r = requests.get(url+uri+name,headers=headers,params={},cert=auth,verify=False).json()
        try:
            test = r["code"]
            print(yaml.dump(r))
        except KeyError:    
            items = list()
            try:
                items = r["items"]
            except KeyError:
                items.append(r)
            if len(items) == 0:
                print("No resources of this type in this namespace")
            else:
                print("NAME\t\tTYPE\t\tCLUSTER-IP\tEXTERNAL-IP\tPORT(S)")
                for elem in items:
                    name = elem["metadata"]["name"]
                    type = elem["spec"]["type"]
                    cluip = elem["spec"]["clusterIP"]
                    extip = "<none>\t"
                    try:
                        extip = elem["spec"]["externalIP"]
                    except:
                        pass
                    ports = ""
                    for port in elem["spec"]["ports"]:
                        if ports != "":
                            ports+=";"
                        ports += str(port["port"])+":"+str(port["targetPort"])+"/"+port["protocol"]
                    print(f"{name}\t{type}\t{cluip}\t{extip}\t{ports}")
        input()
        services()
    elif choice.lower() in ("2","decrire","décrire","describe"):
        name = input("Entrez le nom du service (laisser vide pour tous) : ")
        clear()
        print(yaml.dump(requests.get(url+uri+name,headers=headers,params={},cert=auth,verify=False).json()))
        input()
        services()        
    elif choice.lower() in ("3","supprimer","delete"):
        name = input("Entrez le nom du service (\"q\" pour quitter): ")
        name = name.replace(" ", "")
        if name != "q":
            if dname != "":
                print(yaml.dump(requests.delete(url+uri+name,headers=headers,data={},cert=auth,verify=False).json()))
            else:
                print("Le nom ne peut pas être vide")
            input()
        services()
    elif choice.lower() in ("4","revenir"):
        menu()
    elif choice.lower() in ("5","quitter"):
        return
    else:
        services()
    return

def apply():
    clear()
    filepath = input("Entrez le chemin du fichier (tapez \"q\" pour quitter) : ")
    filepath = filepath.replace(" ", "")
    if filepath == "q" or filepath == "":
        menu()
    else:
        try:
            with open(filepath,"r") as file:
                conf = yaml.safe_load_all(file)
                for elem in conf:
                    apiversion = ""
                    if elem["apiVersion"] == "v1":
                        apiversion = "api/v1"
                    else:
                        apiversion = "apis/"+elem["apiVersion"]
                    uri = apiversion+"/namespaces/"+currnamespace+"/"+elem["kind"].lower()+"s"
                    #print(elem)
                    #print(url+uri)

                    #print()
                    r = requests.put(url+uri+"/"+elem["metadata"]["name"],headers=headers,data=yaml.dump(elem),cert=auth,verify=False).json()
                    try: 
                        r["code"] != None
                        if r["code"] == 404:
                            print(yaml.dump(requests.post(url+uri,headers=headers,data=yaml.dump(elem),cert=auth,verify=False).json()))
                        else:
                            print(yaml.dump(r))
                    except:
                        print(yaml.dump(r))
        except Exception as e:
            print(e)
        input()
        menu()

def delete():
    clear()
    filepath = input("Entrez le chemin du fichier (tapez \"q\" pour quitter) : ")
    filepath = filepath.replace(" ", "")
    if filepath == "q" or filepath == "":
        menu()
    else:
        try:
            with open(filepath,"r") as file:
                conf = yaml.safe_load_all(file)
                for elem in conf:
                    apiversion = ""
                    if elem["apiVersion"] == "v1":
                        apiversion = "api/v1"
                    else:
                        apiversion = "apis/"+elem["apiVersion"]
                    uri = apiversion+"/namespaces/"+currnamespace+"/"+elem["kind"].lower()+"s/"+elem["metadata"]["name"]
                    #print(elem)
                    print(yaml.dump(requests.delete(url+uri,headers=headers,data={},cert=auth,verify=False).json()))
        except Exception as e:
            print(e)
        input()
        menu()

geturl()