###########################################################################
# Description:
#
# Copyright (c) 2025 Nokia
###########################################################################

import json
from collections import OrderedDict

import utilities

# list of traps that will be echoed back to the
traps_list_db: list = []

IFOPERSTATUS_UP             = 1
IFOPERSTATUS_DOWN           = 2
IFOPERSTATUS_TESTING        = 3
IFOPERSTATUS_UNKNOWN        = 4

def convertOperStatus(value: str) -> int:
    if value is not None:
        if value == 'up':
            return IFOPERSTATUS_UP
        elif value == 'down' or value == 'testing' : # RFC2863 section 3.1.15
            return IFOPERSTATUS_DOWN
    return IFOPERSTATUS_UNKNOWN


def store_value_in_json(json_obj:dict, name:str, value) -> None:
    if value is not None:
        json_obj[name] = value


def gRPCServerUpgRPCServerDownTrap(system: list, trap: dict) -> None:
    trap_name = trap.get('name')
    if trap_name is not None:
        row = OrderedDict()
        objects = OrderedDict()

        objects["gRPCServerName"] = system["grpc-server"][0]["name"]

        row['trap'] = trap_name
        row['indexes'] = OrderedDict()  # no indexes to report
        row['objects'] = objects
        traps_list_db.append(row)


#
# main routine
#
def snmp_main(in_json_str: str) -> str:
    global traps_list_db

    in_json = json.loads(in_json_str)

    del in_json_str

    # read in general info from the snmp server
    snmp_info = in_json.get('_snmp_info_')
    utilities.process_snmp_info(snmp_info)

    # read in info about the traps that will be triggered in this request (depending on the trigger)
    trap_info = in_json.get('_trap_info_')

    # read in context data
    system = in_json.get('system', [])

    del in_json

    for trap in trap_info:
        name = trap['name']
        trigger = trap['trigger']
        #print(f'do trap {name} for {trigger}')

        if utilities.is_simulated_trap():
            if name == 'gRPCServerDown':
                gRPCServerUpgRPCServerDownTrap(system, trap)
            elif name == 'gRPCServerUp':
                gRPCServerUpgRPCServerDownTrap(system, trap)
            else:
                raise ValueError(f'Unknown trap {name} with trigger {trigger}')

        else:
            if name == 'gRPCServerDown':
                gRPCServerUpgRPCServerDownTrap(system, trap)
            elif name == 'gRPCServerUp':
                gRPCServerUpgRPCServerDownTrap(system, trap)
            else:
                raise ValueError(f'Unknown trap {name} with trigger {trigger}')

    response:dict = {}

    response['traps'] = traps_list_db

    del system, traps_list_db

    return json.dumps(response)