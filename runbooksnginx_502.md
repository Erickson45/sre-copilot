# Troubleshooting: Nginx 502 Bad Gateway

## Descrição
O erro 502 Bad Gateway no Nginx geralmente indica que o Nginx (atuando como proxy reverso) não conseguiu se comunicar com o serviço de backend (ex: Gunicorn, PHP-FPM, Node).

## Causas Comuns
1. O serviço de backend está inativo ou crashou.
2. O socket ou porta configurada no `nginx.conf` está incorreta.
3. Sobrecarga de recursos (OOM Killer matou o backend).

## Plano de Ação (Comandos)
1. Verificar status do backend: `systemctl status <nome-do-backend>`
2. Checar os logs de erro do Nginx: `tail -n 50 /var/log/nginx/error.log`
3. Verificar uso de memória: `dmesg -T | egrep -i 'killed process'`
4. Reiniciar os serviços: `systemctl restart <nome-do-backend> && systemctl restart nginx`