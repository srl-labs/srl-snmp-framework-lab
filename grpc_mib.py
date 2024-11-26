#!/usr/bin/python
###########################################################################
# Description:
#
# Copyright (c) 2024 Nokia
###########################################################################

import json

import utilities

SERVER_ADMINS_TATUS_UP = 1
SERVER_ADMIN_STATUS_DOWN = 2

IF_OPER_STATUS_UP = 1
IF_OPER_STATUS_DOWN = 2


# maps the gNMI admin status value to its corresponding SNMP value
def convertAdminStatus(value: str):
    if value is not None:
        if value == "enable":
            return SERVER_ADMINS_TATUS_UP
        elif value == "disable":
            return SERVER_ADMIN_STATUS_DOWN


# maps the gNMI oper status value to its corresponding SNMP value
def convertOperStatus(value: str):
    if value is not None:
        if value == "up":
            return IF_OPER_STATUS_UP
        elif value == "down":
            return IF_OPER_STATUS_DOWN


#
# main routine
#
def snmp_main(in_json_str: str) -> str:
    in_json = json.loads(in_json_str)

    del in_json_str

    # read in general info from the snmp server
    snmp_info = in_json.get("_snmp_info_")
    utilities.process_snmp_info(snmp_info)

    # prepare the output dict
    output = {"tables": {"gRPCServerTable": []}}

    # Iterate over all grpc-server instances
    grpc_servers = in_json.get("system", {}).get("grpc-server", [])
    for server in grpc_servers:
        # Extract required fields
        name = server.get("name", "")
        statistics = server.get("statistics", {})
        access_rejects = statistics.get("access-rejects", 0)
        access_accepts = statistics.get("access-accepts", 0)

        last_access_accept = 0
        # Grab the last-access-accept timestamp
        if statistics.get("last-access-accept", False):
            ts = utilities.parse_rfc3339_date()
            # Convert it to timeTicks from boot time
            last_access_accept = utilities.convertUnixTimeStampInTimeticks(ts)

        # Append the object to the output
        output["tables"]["gRPCServerTable"].append(
            {
                "objects": {
                    "gRPCServerName": name,
                    "grpcServerNetworkInstance": server.get("network-instance", ""),
                    "grpcServerAdminState": convertAdminStatus(
                        server.get("admin-state", "")
                    ),
                    "grpcServerOperState": convertOperStatus(server.get("oper-state")),
                    "grpcServerAccessRejects": access_rejects,
                    "grpcServerAccessAccepts": access_accepts,
                    "grpcServerLastAccessAccept": last_access_accept,
                }
            }
        )

    return json.dumps(output)
