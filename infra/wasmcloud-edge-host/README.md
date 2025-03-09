# Wasmcloud Edge Deployment

## NATS Leaf

Creare il nodo `nats-leaf` utilizzando il docker-compose (modificare `nats-leaf.conf` se necessario)

```bash
docker compose up -d
```
Controllare la connessione a Nats
```bash
nast server check connection
```

## Wasmcloud Host

Creare l'host wasmcloud con il comando
```bash
wash up -d --multi-local
```
Controllare il corretto deployment dell'host
```bash
wash get inventory
```
Aggiungere la label all'host
```bash
wash label <host-id> host-type=edge
```