# Zabbix-memory usage

Toolkit to enable effective monitoring with Zabbix use of memory by individual users.

There is the ansible role, which configures Zabbix agent for monitoring memory. As well as a script that creates a Zabbix graph using a low level discovered items.

![Example graph](/example-graph.png?raw=true "Example graph")

### Prerequisites

To use this software do you need Zabbix server and least one Zabbix agent running. You must have administrative privileges to make changes in the configuration of these tools.

### Installing

To run the project, use the Ansible role to install script ``/ansible_role/templates/zabbix_memory.py`` and provide ``linux_memory.rss[*]`` and ``linux_memory.discovery_user`` user parameter in Zabbix Agent.

You can use for that following playbook:

```
---
- hosts: all
  sudo: yes
  roles:
    - role: zabbix_memory_usage
```

Next to import ``/zbx_export_templates.xml`` in Zabbix server and use fresh ``Template memory usage`` template in some server.

Identify: 
* ID of prototype item rule by Configuration-> Hosts -> some.host.example.com -> Discovery rules -> `` Discovery system users`` and lookup URL,
* ID of host by Configuration -> Host -> some.host.example.com and lookup URL. 

After collection some data use ``zabbix-discovered-chart.py`` to add chart by execution eg. ``python zabbix-discovered-chart.py **URL** **LOGIN** **PASS** **ITEMID** **HOSTID**``.

After all new diagram of name "Memory usage graph" should occurs in Zabbix server. See ``zabbix-discovered-chart.py --help`` for details.

## Deployment

Add additional notes about how to deploy this on a live system

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

