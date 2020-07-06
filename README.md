# Cisco Devnet Marathon Day2

## Task
The task is to write a script which searches for an endpoint mac address in a network. Network is a random topology
representing layer 2 domain with a bunch of clients connected to it. Client is considered to be any endpoint connected
to the switch's any untagged interface (_access_) or an SVI belonging to a switch itself. The script has to take a 
mac address as an input and return the switch and corresponding interface name where the requested endpoint mac address
is connected to.

## Script description

Solution uses [_nornir_](https://nornir.readthedocs.io/en/latest/index.html) framework and its [_scrapli_](https://github.com/carlmontanari/scrapli) ssh client integration 
in particular. Script collects some show commands outputs form a device, parses it via [_textfsm_](https://github.com/networktocode/ntc-templates) to get structured data 
and performs a search action.

You need to install the requirements first.

`pip install -r requirements.txt`

To run the script you need to provide the desired mac address as an argument. The format of the argument is strict -
_xxxx.yyyy.zzzz_ lower case (Cisco mac address-table address format). The script does not perform mac format 
normalization as it is out of scope of the task. However it would be a good thing to have in general.

`python mac_address_search.py d89d.6714.cfd4`

result:

`MAC Address d89d.6714.cfd4 is connected to switch SW3 interface Gi1/0/5`





