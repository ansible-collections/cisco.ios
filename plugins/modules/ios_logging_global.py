#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2021 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The module file for ios_logging_global
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
module: ios_logging_global
version_added: 2.1.0
short_description: Manages logging attributes of Cisco IOS network devices
description: This module manages the logging attributes of Cisco IOS network devices.
author: Sagar Paul (@KB-perByte)
options:
  config:
    description: A list containing dictionary of logging options
    type: list
    elements: dict
    suboptions:
      buffered:       
        description: Set buffered logging parameters
        type: dict
        suboptions:
          size: &size           
            description: Logging buffer size
            type: int
          severity: &severity
            description: Logging severity level
            type: str
            choices: &severity_subgroup
              - alerts
              - critical
              - debugging
              - emergencies
              - errors
              - informational
              - notifications
              - warnings
          discriminator: &discriminator   
            description: Establish MD-Buffer association
            type: str
          filtered: &filtered        
            description: Enable filtered logging
            type: bool
          xml: &xml             
            description: Enable logging in XML to XML logging buffer
            type: bool
      buginf:          
        description: Enable buginf logging for debugging
        type: bool
      cns_events:   
        description: Set CNS Event logging level
        type: str
        choices: *severity_subgroup
      console:         
        description: Set console logging parameters
        type: dict
        suboptions:         
          severity:
            description: Logging severity level
            type: str
            choices: ["alerts","critical","debugging","emergencies","errors","informational","notifications","warnings","guaranteed"]
          discriminator: *discriminator   
          filtered: *filtered       
          xml: *xml            
      count:                
        description: Count every log message and timestamp last occurance
        type: bool
      delimiter:    
        description: Append delimiter to syslog messages
        type: dict
        suboptions:
          tcp:           
            description: Append delimiter to syslog messages over TCP
            type: bool
      discriminator:
        description: Create or modify a message discriminator
        type: str
      dmvpn:          
        description: DMVPN Configuration
        type: dict
        suboptions:
          rate_limit: &rate_limit          
            description: rate in messages/minute, default is 600 messages/minute (1-10000)
            type: int
      esm:        
        description: Set ESM filter restrictions
        type: dict
        suboptions:
          config:           
            description: Permit/Deny configuration changes from ESM filters
            type: bool
      exception:    
        description: Limit size of exception flush output (4096-2147483647)
        type: int
      facility:     
        description: Facility parameter for syslog messages
        type: str
        choices: ["auth","cron","daemon","kern","local0","local1","local2","local3","local4","local5","local6","local7","lpr","mail","news","sys10","sys11","sys12","sys13","sys14","sys9","syslog","user","uucp"]
      filter:     
        description: Specify logging filter
        type: list
        elements: dict
        suboptions:
          url: 
            description: Filter Uniform Resource Locator
            type: str
          order: 
            description: Order of filter execution
            type: int
          args:
            description: Arguments passed to filter module.
            type: str
      history:
        description: Configure syslog history table
        type: dict
        suboptions:     
          size: *size          
          severity: *severity
      host:           
        description: Set syslog server IP address and parameters
        type: list
        elements: dict
        suboptions:          
          discriminator: *discriminator
          filtered: *filtered
          sequence_num_session: &sequence_num_session
            description: Include session sequence number tag in syslog message
            type: bool
          session_id: &session_id
            description: Specify syslog message session ID tagging
            type: dict
            suboptions: &session_id_suboptions
              tag: 
                description: Include hostname in session ID tag
                type: str
                choices: ["hostname","ip","ipv6"]
              text: 
                description: Include custom string in session ID tag
                type: str
          transport: &transport
            description: Specify the transport protocol (default=UDP)
            type: dict
            suboptions:
              tcp:
                description: Transport Control Protocol
                type: dict
                suboptions:
                  audit:
                    description: Set this host for IOS firewall audit logging
                    type: bool
                  discriminator: *discriminator
                  filtered:
                    description: Enable filtered logging
                    type: dict
                    suboptions:
                      stream: 
                        description: This server should only receive messages from a numbered stream
                        type: int
                  port:
                    description: Specify the TCP port number (default=601) (1 - 65535)
                    type: int
                  sequence_num_session: *sequence_num_session
                  session_id: *session_id
                  xml: *xml
              udp:
                description: User Datagram Protocol
                type: dict
                suboptions:
                  discriminator: *discriminator
                  filtered:
                    description: Enable filtered logging
                    type: dict
                    suboptions:
                      stream: 
                        description: This server should only receive messages from a numbered stream
                        type: int
                  port:
                    description: Specify the TCP port number (default=601) (1 - 65535)
                    type: int
                  sequence_num_session: *sequence_num_session
                  session_id: *session_id
                  xml: *xml
          vrf:
            description: Set VRF option
            type: str
          xml: *xml
          stream:
            description: This server should only receive messages from a numbered stream
            type: int 
          ipv6:            
            description: Configure IPv6 syslog server
            type: str
          hostname:
            description: IP address of the syslog server
            type: str
      message_counter:   
        description: Configure log message to include certain counter value
        type: list
        elements: str
        choices: ["log", "debug", "syslog"]
      monitor:        
        description: Set terminal line (monitor) logging parameters
        type: dict
        suboptions:        
          severity: *severity
          discriminator: *discriminator  
          filtered: *filtered        
          xml: *xml              
      logging_on:               
        description: Enable logging to all enabled destinations
        type: bool
      origin_id:      
        description: Add origin ID to syslog messages
        type: dict
        suboptions: *session_id_suboptions
      persistent:
        description: Set persistent logging parameters
        type: dict
        suboptions:
          batch:      
            description: Set batch size for writing to persistent storage (4096-2142715904)
            type: int
          filesize:   
            description: Set size of individual log files (4096-2142715904)
            type: int
          immediate:  
            description: Write log entry to storage immediately (no buffering).
            type: bool
          notify:
            description: Notify when show logging [persistent] is activated.
            type: bool
          protected:
            description: Eliminates manipulation on logging-persistent files.
            type: bool
          size:       
            description: Set disk space for writing log messages (4096-2142715904)
            type: int
          threshold:  
            description: Set threshold for logging persistent
            type: int
          url:        
            description: URL to store logging messages
            type: str 
      policy_firewall:   
        description: Firewall configuration
        type: dict
        suboptions:
          rate_limit:
            description: (0-3600) value in seconds, default is 30 Sec.
            type: int
      queue_limit:     
        description: Set logger message queue size
        type: dict
        suboptions:
          size:
            description: (100-2147483647) set new queue size
            type: int
          esm:
            description: (100-2147483647) set new queue size
            type: int
          trap:
            description: (100-2147483647) set new queue size
            type: int
      rate_limit:           
        description: Set messages per second limit
        type: dict
        suboptions:
          size: &rate_limit_size
            description: (1-10000) message per second
            type: int
            required: True
          all:
            description: (1-10000) message per second
            type: bool
          console:
            description: (1-10000) message per second
            type: bool
          except:
            description: Messages of this severity or higher
            type: str
            choices: *severity_subgroup
      reload:        
        description: Set reload logging level
        type: dict
        suboptions:      
          severity: *severity
          message_limit:
            description: Number of messages (1-4294967295>)
            type: int
      server_arp:        
        description: Enable sending ARP requests for syslog servers when first configured
        type: bool
      snmp_trap:   
        description: Set syslog level for sending snmp trap
        type: str
        choices: *severity_subgroup
      source_interface:
        description: Specify interface for source address in logging transactions
        type: list
        elements: dict
        suboptions:
          interface:
            description: Interface name with number
            type: str
          vrf:
            description: VPN Routing/Forwarding intstance name
            type: str
      trap:   
        description: Set syslog server logging level
        type: str
        choices: *severity_subgroup
      userinfo:      
        description: Enable logging of user info on privileged mode enabling
        type: bool
  running_config:
      description:
      - This option is used only with state I(parsed).
      - The value of this option should be the output received from the EOS device by
        executing the command B(show running-config | section access-list).
      - The state I(parsed) reads the configuration from C(running_config) option and
        transforms it into Ansible structured data as per the resource module's argspec
        and the value is then returned in the I(parsed) key within the result.
      type: str
  state:
    choices:
    - merged
    - replaced
    - overridden
    - deleted
    - gathered
    - parsed
    - rendered
    default: merged
    description:
    - The state the configuration should be left in
    type: str
"""
EXAMPLES = """
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.argspec.logging_global.logging_global import (
    Logging_globalArgs,
)
from ansible_collections.cisco.ios.plugins.module_utils.network.ios.config.logging_global.logging_global import (
    Logging_global,
)

# print("Checking logging via VSCode")
# import debugpy
# debugpy.listen(3000)
# debugpy.wait_for_client()

def main():
    """
    Main entry point for module execution

    :returns: the result form module invocation
    """
    module = AnsibleModule(
        argument_spec=Logging_globalArgs.argument_spec,
        mutually_exclusive=[["config", "running_config"]],
        required_if=[
            ["state", "merged", ["config"]],
            ["state", "replaced", ["config"]],
            ["state", "overridden", ["config"]],
            ["state", "rendered", ["config"]],
            ["state", "parsed", ["running_config"]],
        ],
        supports_check_mode=True,
    )

    result = Logging_global(module).execute_module()
    module.exit_json(**result)


if __name__ == "__main__":
    main()
