###########################################################################
# Description:
#
# Copyright (c) 2025 Nokia
###########################################################################

import json
from collections import OrderedDict
import re
import utilities

# list of traps that will be echoed back to the client
traps_list_db: list = []


def parseGrpcServerKeys(xpath: str):
    # retrieve the name of the grpc-server from the xpath
    name_pattern = re.compile(r"[^\]]+\[([^\[\]=]+?)=([^\]]+)\]")
    matches = name_pattern.match(xpath)
    if matches is not None:
        return matches.group(2)
    return None


def gRPCServerUpgRPCServerUpDownTrap(grpc_servers: list, trap: dict, value) -> None:
    filter_key = parseGrpcServerKeys(trap.get("xpath", ""))
    if filter_key is None:
        raise ValueError(f"Can't look for a grpc-server without an xpath")

    # loop over all grpc-servers, filter the ones that match the xpath
    for server in grpc_servers:
        server_name = server.get("name", "")  # key
        if server_name != filter_key:
            continue

        # only report the grpc-servers that have the correct oper-state (unless force flag was used)
        if not utilities.is_forced_simulated_trap():
            oper_state = server.get("oper-state", "")
            if value is not None and oper_state != value:
                continue

        row = OrderedDict()
        objects = OrderedDict()

        objects["gRPCServerName"] = server_name

        row["trap"] = trap.get("name", "")
        row["indexes"] = OrderedDict()  # no indexes to report
        row["objects"] = objects
        traps_list_db.append(row)


#
# main routine
#
def snmp_main(in_json_str: str) -> str:
    global traps_list_db

    in_json = json.loads(in_json_str)

    # read in general info from the snmp server
    snmp_info = in_json.get("_snmp_info_")
    utilities.process_snmp_info(snmp_info)

    # read in info about the traps that will be triggered in this request (depending on the trigger)
    trap_info = in_json.get("_trap_info_", [])

    system = in_json.get("system", {})
    grpc_servers = system.get("grpc-server", [])

    # loop over all traps in this request
    for trap in trap_info:
        name = trap.get("name", "")
        trigger = trap.get("trigger", "")
        newValue = trap.get("new-value", "")

        if name == "gRPCServerDown":
            if newValue == "down" or utilities.is_forced_simulated_trap():
                gRPCServerUpgRPCServerUpDownTrap(grpc_servers, trap, newValue)
        elif name == "gRPCServerUp":
            if newValue == "up" or utilities.is_forced_simulated_trap():
                gRPCServerUpgRPCServerUpDownTrap(grpc_servers, trap, newValue)
        else:
            raise ValueError(f"Unknown trap {name} with trigger {trigger}")

    response: dict = {}

    response["traps"] = traps_list_db

    return json.dumps(response)
