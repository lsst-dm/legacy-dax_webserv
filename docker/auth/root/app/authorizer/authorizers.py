# LSST Data Management System
# Copyright 2018 AURA/LSST.
#
# This product includes software developed by the
# LSST Project (http://www.lsst.org/).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the LSST License Statement and
# the GNU General Public License along with this program.  If not,
# see <http://www.lsstcorp.org/LegalNotices/>.

import logging
import subprocess
from typing import Dict, Any, Tuple

from .config import Config

logger = logging.getLogger(__name__)


# noinspection PyUnusedLocal
def scp_check_access(capability: str, request_method: str, request_path: str,
                     token: Dict[str, Any]) -> Tuple[bool, str]:
    """Check that a user has access with the following operation to this
    service based on the assumption the token has a "scp" claim.
    :param capability: The capability we are checking against
    :param request_method: The operation requested for this service
    :param request_path: The uri that will be tested
    :param token: The token necessary
    :rtype: Tuple[bool, str]
    :returns: (successful, message) with successful as True if the
    scitoken allows for op and the user can read/write the file, otherwise
    return (False, message)
    """
    capabilites = set(token.get("scp"))
    if capability in capabilites:
        return True, "Success"
    return False, f"No capability found: {capability}"


# noinspection PyUnusedLocal
def group_membership_check_access(capability: str, request_method: str, request_path: str,
                                  token: Dict[str, Any]) -> Tuple[bool, str]:
    """Check that a user has access with the following operation to this service
    based on some form of group membership.
    :param capability: The capability we are checking against
    :param request_method: The operation requested for this service
    :param request_path: The uri that will be tested
    :param token: The token necessary
    :rtype: Tuple[bool, str]
    :returns: (successful, message) with successful as True if the
    scitoken allows for op and the user can read/write the file, otherwise
    return (False, message)
    """
    user_groups = token.get("isMemberOf")
    capability_group = _group_membership_get_group(capability)
    if capability_group in user_groups:
        return True, "Success"
    return False, "No Capability group found in user's `isMemberOfGroups`"


def _group_membership_get_group(capability: str) -> str:
    """
    Given a capability, find a group that represents this capability.
    :param capability: The capability in question
    :return: A string value of the group for this capability.
    """
    group = Config.GROUP_MAPPING.get(capability)
    assert capability is not None, "Error: Capability not found in group mapping"
    return group


# noinspection PyUnusedLocal
def webdav_check_access(capability: str, request_method: str, request_path: str,
                        token: Dict[str, Any]) -> Tuple[bool, str]:
    """Check that a user has access with the following operation to this service
    and the file path in question for a WebDAV service.
    :param capability: The capability we are checking against
    :param request_method: The operation requested for this service
    :param request_path: The uri that will be tested
    :param token: The token necessary
    :returns: (successful, message) with successful as True if the
    scitoken allows for op and the user can read/write the file, otherwise
    return (False, message)
    """

    # Check Impersonation Next
    service_path = Config.WEBDAV_SERVICE_PATH
    assert request_path.startswith(service_path), "ERROR: Nginx WebDAV misconfiguration"

    # Now remove the base request_path so we just get the auth_path + request_path
    filepath_on_disk = request_path.replace(service_path, "", 1)
    (op, _) = capability.split(":")

    webdav_authorizer = Config.WEBDAV_AUTHORIZERS[Config.WEBDAV_AUTHORIZER]
    if webdav_authorizer(token, op, filepath_on_disk):
        return True, ""
    return False, "Path not allowed"


# noinspection PyUnusedLocal
def webdav_null_authorizer(token: Dict[str, Any], op: str, filepath_on_disk: str) -> bool:
    return True


def webdav_sudo_authorizer(token: Dict[str, Any], op: str, filepath_on_disk: str) -> bool:
    test_option = "-w" if op == "write" else "-r"
    params = ["sudo", "-u", token["sub"], "test", test_option, filepath_on_disk]
    logger.debug("Executing Impersonation Test: " + " ".join(params))
    return_code = subprocess.call(params)
    return return_code == 0
