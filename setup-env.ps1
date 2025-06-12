# Script para configurar o arquivo .env

# Copiar o arquivo de exemplo
Copy-Item env.example .env

# Obter o endereço IP do Minikube
$minikube_ip = minikube ip

# Atualizar as variáveis no arquivo .env
$env_content = Get-Content .env
$env_content = $env_content -replace 'MLFLOW_TRACKING_URI=.*', "MLFLOW_TRACKING_URI=http://$minikube_ip:5000"
$env_content = $env_content -replace 'KUBERNETES_CLUSTER_URL=.*', "KUBERNETES_CLUSTER_URL=https://$minikube_ip:8443"
$env_content | Set-Content .env

Write-Host "Arquivo .env configurado com sucesso!"
Write-Host "Por favor, verifique o arquivo .env e ajuste outras variáveis conforme necessário." 