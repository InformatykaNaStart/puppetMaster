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
  sio2pm-spawndocker --verbose --paramFile {repoRoot}/configs/master --apiToken {PacketApiToken} --projectId {PacketProjectId} informatykanastart/siomaster
  ```
  and note down the IP of the master server reported in the displayed messages
* Run
  ```
  sio2pm-spawndocker --verbose --paramFile {repoRoot}/configs/worker -s MASTER_IP {ip} --apiToken {PacketApiToken} --projectId {PacketProjectId} informatykanastart/sioworker
  ```
  subsituting the `{ip}` with the IP of the master node you noted down in the previous step and other `{placeholders}` with valid paths/values.

If you are getting a `prices to high` error, try to raise an allowed price using the `--bidMax` parameter. 

## Packet cloud worker for sio2.staszic.waw.pl

* Generate an RSA key pair and add the public key to the `~/.ssh/authorized_keys` on dziobak@sio2.staszic.waw.pl
* Run
  ```
  sio2pm-spawndocker --verbose --tunnelHost sio2.staszic.waw.pl --tunnelUser dziobak --tunnelKey {pathToRsaPrivKey} --paramFile {repoRoot}/configs/worker -s MASTER_IP sio2.staszic.waw.pl --apiToken Z5pqw9cEqvJozrUAWkKi6yfDnfyZqCDA --projectId c3541c08-9b5b-47d7-b7ba-5498a614f267 informatykanastart/sioworker
  ```

## Packet.com related parameters

Use following `sio2pm-spawndocker` parameters to adjust the Packet.com facility and instance price:

* `--facility` the Packet.com facility where the VM'll be created, e.g. `ams1` or `ewr1`
* `--bidMax` highest accepted price - a VM won't be created if the current market prices are higher
* `--bidOver` the price used for bidding on the market is `round(currentMarketPrice * (1 + bidOver), 2)`

