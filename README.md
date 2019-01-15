# PuppetMaster

A simple library for automatic managment of SIO2 workers in the Packet.com cloud.

# Installation

* clone the repo
* enter the repo directory
* run `python3 setup.py build && python3 setup.py install` (may require root rights or a Python virtual environment)

# Usage

## Simple localhost usage

(requires that `siomaster` resolves to `127.0.0.1` and replacement of `{placeholders}` with valid paths/values)

```
sio2pm-spawndocker --verbose --hostName siomaster --paramFile {repoRoot}/configs/master-local informatykanastart/siomaster
sio2pm-spawndocker --verbose --hostName siomaster --paramFile {repoRoot}/configs/worker-local -s MASTER_IP siomaster -s N 1 -s P {nCores} informatykanastart/sioworker
```

## Simple Packet cloud usage

* Run
  ```
  sio2pm-spawndocker --hostName siomaster --verbose --paramFile configs/master --apiToken {PacketApiToken} --projectId {PacketProjectId} informatykanastart/siomaster
  ```
  and note down the IP of the master server reported in the displayed messages
* Run
  ```
  sio2pm-spawndocker --verbose --hostName sioworker --paramFile configs/worker -s MASTER_IP {ip} -s MEMORY_LIMIT 1G -s N_PARALLEL 4 --apiToken {PacketApiToken} --projectId {PacketProjectId} informatykanastart/sioworker
  ```
  subsituting the `{ip}` with the IP of the master node you noted down in the previous step and the `{PacketApiToken}` & `{PacketProjectId}` with your Packet credentials.

