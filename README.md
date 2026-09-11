\# Secure IoT Monitoring Stack



Projet IoT sécurisé et conteneurisé avec Docker.



\## Architecture



Sensor Python → MQTT TLS/mTLS → Mosquitto → Bridge Python → InfluxDB → Grafana



\## Services



\- Mosquitto : broker MQTT sécurisé sur le port 8883

\- Sensor : génération de températures aléatoires

\- Bridge : récupération MQTT et stockage InfluxDB

\- InfluxDB : base de données temporelle

\- Grafana : dashboard de supervision sur le port 3000



\## Sécurité



\- MQTT over TLS

\- Authentification mutuelle par certificats mTLS

\- Chiffrement des messages MQTT

\- Analyse possible avec Wireshark sur le port 8883



\## Démarrage



```powershell

docker compose up -d --build

