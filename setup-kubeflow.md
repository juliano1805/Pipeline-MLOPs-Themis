# Instalação do Kubeflow

## 1. Pré-requisitos

Certifique-se de que o Minikube está rodando:
```powershell
minikube status
```

## 2. Instalar o kustomize

```powershell
# Usando Chocolatey
choco install kustomize
```

## 3. Instalar o Kubeflow usando kustomize

```powershell
# Criar diretório para o Kubeflow
mkdir kubeflow
cd kubeflow

# Baixar o manifesto do Kubeflow
curl -O https://raw.githubusercontent.com/kubeflow/manifests/v1.7.0/kfdef/kfdef_kustomize.yaml

# Aplicar o manifesto
kubectl apply -f kfdef_kustomize.yaml
```

## 4. Verificar a instalação

```powershell
# Verificar os pods do Kubeflow
kubectl get pods -n kubeflow

# Aguardar até que todos os pods estejam em estado Running
kubectl get pods -n kubeflow -w
```

## 5. Acessar o Dashboard do Kubeflow

```powershell
# Expor o serviço do dashboard
kubectl port-forward svc/istio-ingressgateway -n istio-system 8080:80

# Acessar o dashboard em:
# http://localhost:8080
```

## 6. Configurar o acesso ao Kubeflow

```powershell
# Obter a senha padrão
kubectl get secret kubeflow-admin-password -n kubeflow -o jsonpath='{.data.password}' | base64 --decode

# Usar as credenciais:
# Usuário: admin
# Senha: (senha obtida no comando acima)
```

## 7. Verificar os componentes do Kubeflow

```powershell
# Listar todos os componentes instalados
kubectl get pods -n kubeflow

# Verificar o status do pipeline
kubectl get pods -n kubeflow -l app=ml-pipeline
``` 