# Infrastuttura

L'infrastuttura simula un flusso IoT ed è composta da:
- ambiente Cloud, deployato su kubernetes e dotato di cluster NATS, WADM e Wasmcloud Host 
- ambiente Edge, semplice macchina Linux con docker compose, Wasmcloud e NATS Leaf come docker container
- dispositivi IoT collegati all'ambiente Edge

![infra](/project/img/infra.png)

# Pipeline

Il processo si divide in due fasi principali, cioè quello di generazione del componente wasm e quella di deploy.

## Generazione del componente WASM

Questa fase si occupa di trasformare una serie di files descrittivi in codice, selezionare il template corretto, buildare il progetto, generare il file di deploy e quindi pushare l'artifact OCI in un registry.

### Parsing del codice

Il progetto di partenza è composto da un file `workflow.yaml`, nel quale vengono descritti tutti i componenti, e da una cartella `tasks` contenente le porzioni di codice che devono essere eseguite dai vari componenti.

```
├─ workflow.yaml
└─ tasks
   ├─ sensor_read.go
   ├─ aggregate.go
   └─ db_sync.go
```

#### Workflow
Nel file workflow vengono descritti i vari componenti, un esempio potrebbe essere

```yaml
tasks:
  - name: Data Aggregation                # Displayed name
    type: processing                      # Used to select template
    code: aggregate.go                    # Go code file inside tasks/ dir
    target:                               # Where the component will be deployed
      - edge
      - cloud
    source_topic: temp_sensor             # Source NATS topic
    dest_topic: aggregated_data           # Destination NATS topic
    component_name: data_aggregation      # Component name displayed in the OCI artifact
    version: 1.0.0                        # Component version
...
```
