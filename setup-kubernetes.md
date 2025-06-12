# Configuração do Kubernetes com Minikube

## 1. Instalar o Minikube

### Windows (usando PowerShell como administrador):
```powershell
# Instalar o Chocolatey primeiro (se ainda não tiver)
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Instalar o Minikube
choco install minikube

# Instalar o kubectl
choco install kubernetes-cli
```

### Verificar a instalação:
```powershell
minikube version
kubectl version
```

## 2. Iniciar o cluster Minikube

```powershell
# Iniciar o cluster com recursos adequados
minikube start --cpus 4 --memory 8192 --driver=hyperv

# Verificar o status
minikube status
```

## 3. Configurar o namespace para o projeto

```powershell
# Criar o namespace mlops
kubectl create namespace mlops

# Verificar se foi criado
kubectl get namespaces
```

## 4. Configurar o acesso ao cluster

```powershell
# Obter a configuração do cluster
minikube kubectl -- config view --flatten > kubeconfig.yaml

# Configurar o kubectl para usar o arquivo
$env:KUBECONFIG="kubeconfig.yaml"
```

## 5. Verificar a instalação

```powershell
# Verificar os nós do cluster
kubectl get nodes

# Verificar os pods do sistema
kubectl get pods -n kube-system
``` 