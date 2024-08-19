# Scope of project
Tha annotation must tell the splitter how to aggregate and where to send each task.

## Possible implementation

The code will be processed and splitted into possible modules. Inside the path /build will be created a directory for each module. Inside there will be the wasm compiled bytecode, a file scheduler.config that will list all the information that schedule could need to schedule the module.


## Targets
Possible devices that run the task:
- Cloud device, prossibly the same cloud that runs the scheduler
- Edge device
- IoT device, the only one that can run device specific tasks

## Annotations

List of possible annotations:

- `@TaskGeneric` defines a generic task that can run everywere
- `@CloudSpecific` runs only on cloud
- `@EdgeSpecific` runs only on edge
- `@EndDeviceSpecific` runs only on end device, in particular the device can be specified with `@EndDeviceSpecific(device_name)`
