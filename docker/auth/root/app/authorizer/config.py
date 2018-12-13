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


import configparser
import errno
import json
import logging
import re
from typing import Dict, List

logger = logging.getLogger(__name__)


class Config:
    GLOBAL_AUDIENCE = ""
    AUTHORIZED_ISSUERS = {}
    DEFAULT_RESOURCE = ""
    ALGORITHM = "RS256"
    JWT_OPTIONS = {}
    RESOURCE_CHECKS: Dict[str, List] = {"default": ["group_membership"]}
    NO_VERIFY = False
    NO_AUTHORIZE = False
    REALM = "tokens"
    WWW_AUTHENTICATE = "Bearer"

    WEBDAV_SERVICE_PATH = ""
    WEBDAV_AUTHORIZER = "sudo"
    GROUP_DEPLOYMENT_PREFIX = "lsst_"
    GROUP_MAPPING = {}

    WEBDAV_AUTHORIZERS = {}

    CHECK_ACCESS_CALLABLES = {}

    @staticmethod
    def configure_plugins():
        from .authorizers import webdav_null_authorizer, webdav_sudo_authorizer
        from .authorizers import scp_check_access, group_membership_check_access, \
            webdav_check_access
        from .lsst import lsst_group_membership_check_access

        Config.WEBDAV_AUTHORIZERS = {
            "none": webdav_null_authorizer,
            "sudo": webdav_sudo_authorizer
        }

        Config.CHECK_ACCESS_CALLABLES = {
            "scp": scp_check_access,
            "group_membership": group_membership_check_access,
            "webdav": webdav_check_access,
            "lsst_group_membership": lsst_group_membership_check_access
        }

    @staticmethod
    def load(fname):
        global logger
        Config.configure_plugins()
        logger.info("Loading configuration from %s" % fname)
        cp = configparser.ConfigParser()
        try:
            with open(fname, "r") as fp:
                cp.read_file(fp)
        except IOError as ie:
            if ie.errno == errno.ENOENT:
                return
            raise

        # Logging
        if "loglevel" in cp.options("Global"):
            level = cp.get("Global", "loglevel")
            logger.info(f"Reconfiguring log, level={level}")
            # Reconfigure logging
            for handler in logging.root.handlers[:]:
                logging.root.removeHandler(handler)
            logging.basicConfig(level=level)
            logger = logging.getLogger(__name__)
            if level == "DEBUG":
                logging.getLogger('werkzeug').setLevel(level)

        # Globals
        if 'audience_json' in cp.options("Global"):
            # Read in the audience as json.  Hopefully it's in list format or a string
            Config.GLOBAL_AUDIENCE = json.loads(cp.get("Global", "audience_json"))
        elif 'audience' in cp.options("Global"):
            Config.GLOBAL_AUDIENCE = cp.get("Global", "audience")
            if ',' in Config.GLOBAL_AUDIENCE:
                # Split the audience list
                Config.GLOBAL_AUDIENCE = re.split("\s*,\s*", Config.GLOBAL_AUDIENCE)

        if 'default_resource' in cp.options("Global"):
            Config.DEFAULT_RESOURCE = cp.get("Global", "default_resource")

        if 'realm' in cp.options("Global"):
            Config.REALM = cp.get("Global", "realm")
            logger.info(f"Configured realm {Config.REALM}")

        if 'www_authenticate' in cp.options("Global"):
            Config.WWW_AUTHENTICATE = cp.get("Global", "www_authenticate")
            logger.info(f"Configured WWW-Authenticate type: {Config.WWW_AUTHENTICATE}")

        if "no_verify" in cp.options("Global"):
            Config.NO_VERIFY = cp.getboolean("Global", "no_verify")
            logger.warning("Authentication verification is disabled")

        if "no_authorize" in cp.options("Global"):
            Config.NO_AUTHORIZE = cp.getboolean("Global", "no_authorize")
            logger.warning("Authorization is disabled")

        if 'webdav_service_path' in cp.options("Global"):
            webdav_service_path = cp.get("Global", "webdav_service_path")
            Config.WEBDAV_SERVICE_PATH = webdav_service_path
            logger.info(f"Configured WebDAV service path as: {webdav_service_path}")
        else:
            logger.warning("No WebDAV service path defined for application")

        if 'webdav_authorizer' in cp.options("Global"):
            authorizer = cp.get("Global", "webdav_authorizer")
            if authorizer not in Config.WEBDAV_AUTHORIZERS:
                raise Exception("No Valid WebDAV authorizer found")
            Config.WEBDAV_AUTHORIZER = authorizer
            logger.info(f"Configured WebDAV authorizer: {authorizer}")

        if 'group_deployment_prefix' in cp.options("Global"):
            prefix = cp.get("Global", "group_deployment_prefix")
            Config.GROUP_DEPLOYMENT_PREFIX = prefix
            logger.info(f"Configured LSST Group Deployment Prefix: {prefix}")

        if 'group_mapping' in cp.options("Global"):
            mapping = json.loads(cp.get("Global", "group_mapping"))
            for key, value in mapping.items():
                assert isinstance(key, str) and isinstance(value, str), "Mapping is malformed"
            Config.GROUP_MAPPING = mapping
            logger.info(f"Configured Group Mapping: {mapping}")

        # Find JWT options
        for option_name in cp.options("Global"):
            if option_name.startswith("jwt_"):
                key = option_name[len("jwt_"):]
                value = cp.get("Global", option_name)
                Config.JWT_OPTIONS[key] = value

        # Find Resource Check Callables
        for option_name in cp.options("Global"):
            if option_name.startswith("resource_checks_"):
                key = option_name[len("resource_checks_"):]
                values = json.loads(cp.get("Global", option_name))
                if not isinstance(values, list):
                    raise Exception("Resource checks not a list:")
                for callable_name in values:
                    if callable_name not in Config.CHECK_ACCESS_CALLABLES:
                        raise Exception(f"No access checker for id {callable_name}")
                Config.RESOURCE_CHECKS[key] = values
        for resource, callables in Config.RESOURCE_CHECKS.items():
            logger.info(f"Configured resource checks: {resource} - {callables}")

        # Sections
        for section in cp.sections():
            logger.debug(f"Processing Section {section}")
            if not section.lower().startswith("issuer "):
                continue
            if 'issuer' not in cp.options(section):
                logger.warning(f"Ignore section {section} as it has no `issuer`")
                continue
            issuer = cp.get(section, 'issuer')

            issuer_info = Config.AUTHORIZED_ISSUERS.setdefault(issuer, {})
            issuer_info["issuer_key_id"] = cp.get(section, 'issuer_key_id')
            # if 'map_subject' in cp.options(section):
            #     issuer_info['map_subject'] = cp.getboolean(section, 'map_subject')
            logger.info(f"Configured token access for {section} (issuer {issuer}): {issuer_info}")
        logger.info("Configured Issuers")
