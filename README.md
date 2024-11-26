# SR Linux SNMP Framework

SNMP, powered by gNMI. This is the way.

[Read more.](https://learn.srlinux.dev/snmp/snmp_framework/)

Deploy the lab

```
sudo containerlab deploy -t srl-labs/srl-snmp-framework-lab
```

Try the new MIB:

```bash
docker run --init --network clab -i -t goatatwork/snmpwalk \
-v 2c -c public snmp-srl 1.3.6.1.4.1.6527.115
```
