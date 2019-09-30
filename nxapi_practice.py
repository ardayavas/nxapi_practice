import requests, json
import config as c
from nxapilib import nxapi_req

host = c.host
cred = c.cred

def cmdin(cmd):
    res = requests.post('http://' + host + '/ins',
                        auth=cred,
                        headers={'content-type': 'application/json'},
                        data=nxapi_req('cli_show', cmd))
    return json.loads(res.text)

def cmdcreate(cmd):
    res = requests.post('http://' + host + '/ins',
                        auth=cred,
                        headers={'content-type': 'application/json'},
                        data=nxapi_req('cli_conf', cmd))
    return json.loads(res.text)

def getinterfacesofvlan(i,vlanid):
    vlan = i.get('ins_api').get('outputs').get('output').get('body').get('TABLE_vlanbriefxbrief').get('ROW_vlanbriefxbrief')

    for hede in vlan:
        if hede.get('vlanshowbr-vlanid') == vlanid:
            return hede.get('vlanshowplist-ifidx').split(',')

def findinterfacewithdescKC(inlist):
    iflist = []
    allif = inlist.get('ins_api').get('outputs').get('output').get('body').get('TABLE_interface').get('ROW_interface')

    for intf in allif:
        if intf.get('desc') == 'KC':
            iflist.append(intf.get('interface'))
    return iflist

### MAIN ###

out = cmdin('show vlan brief')
interfacelist = getinterfacesofvlan(out,c.src_vlan)

out = cmdin('show interface description')
intwithdesc = findinterfacewithdescKC(out)

out = cmdcreate('vlan {}'.format(c.dest_vlan))
print(out)

for a in interfacelist:
    if a in intwithdesc:
        cmd = 'interface {} ;switchport access vlan {}'.format(a,c.dest_vlan)
        print(a)
        print(cmdcreate(cmd))
