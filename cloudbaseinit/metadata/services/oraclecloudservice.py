# TODO: license info

from oslo_log import log as oslo_logging

from cloudbaseinit import conf as cloudbaseinit_conf
from cloudbaseinit.metadata.services import base
from cloudbaseinit.utils import network

from base64 import b64decode

CONF = cloudbaseinit_conf.CONF
LOG = oslo_logging.getLogger(__name__)


class OracleCloudService(base.BaseHTTPMetadataService):
    _metadata_version = 'v2'
    _headers = {"Authorization": "Bearer Oracle"}

    def __init__(self):
        super(OracleCloudService, self).__init__(
            base_url=CONF.oraclecloud.metadata_base_url,
            https_allow_insecure=CONF.oraclecloud.https_allow_insecure,
            https_ca_bundle=CONF.oraclecloud.https_ca_bundle)
        self._enable_retry = True

    def load(self):
        super(OracleCloudService, self).load()
        if CONF.oraclecloud.add_metadata_private_ip_route:
            network.check_metadata_ip_route(CONF.oraclecloud.metadata_base_url)

        try:
            self.get_instance_id()
            return True
        except Exception as ex:
            LOG.exception(ex)
            LOG.debug('Metadata not found at URL \'%s\'' %
                      CONF.oraclecloud.metadata_base_url)
            return False

    def get_instance_id(self):
        return self._get_cache_data('opc/%s/instance/id' %
                                    self._metadata_version,
                                    headers=self._headers)

    def get_user_data(self):
        return b64decode(self._get_cache_data('opc/%s/instance/metadata/user_data' %
                                    self._metadata_version,
                                    headers=self._headers))

    def get_host_name(self):
        return self._get_cache_data('opc/%s/instance/hostname' %
                                    self._metadata_version,
                                    headers=self._headers)
