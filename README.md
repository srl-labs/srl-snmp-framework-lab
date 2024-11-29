# SR Linux SNMP Framework

SNMP, powered by gNMI. This is the way.

[Read more.](https://learn.srlinux.dev/snmp/snmp_framework/)

---
<div align=center markdown>
<a href="https://codespaces.new/srl-labs/srl-snmp-framework-lab?quickstart=1&devcontainer_path=.devcontainer%2Fdocker-in-docker%2Fdevcontainer.json">
<img src="https://gitlab.com/rdodin/pics/-/wikis/uploads/d78a6f9f6869b3ac3c286928dd52fa08/run_in_codespaces-v1.svg?sanitize=true" style="width:50%"/></a>

**Run this lab in GitHub Codespaces for free**.  
[Learn more](https://containerlab.dev/manual/codespaces) about Containerlab for Containerlab.  
<small>Machine type: 2 vCPU · 8 GB RAM</small>
</div>

---

Deploy the lab

```
sudo containerlab deploy -t srl-labs/srl-snmp-framework-lab
```

Try the new MIB:

```bash
docker run --init --network clab -i -t goatatwork/snmpwalk \
-v 2c -c public snmp-srl 1.3.6.1.4.1.6527.115
```
