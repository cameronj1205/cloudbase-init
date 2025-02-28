# TODO: license info

"""Config options available for the Oracle Cloud metadata service."""

from oslo_config import cfg

from cloudbaseinit.conf import base as conf_base


class OracleCloudOptions(conf_base.Options):

    """Config options available for the OpenStack metadata service."""

    def __init__(self, config):
        super(OracleCloudOptions, self).__init__(config, group="oraclecloud")
        self._options = [
            cfg.StrOpt(
                "metadata_base_url", default="http://169.254.169.254/",
                help="The base URL where the service looks for metadata",
                deprecated_group="DEFAULT"),
            cfg.BoolOpt(
                "add_metadata_private_ip_route", default=True,
                help="Add a route for the metadata ip address to the gateway",
                deprecated_group="DEFAULT"),
            cfg.BoolOpt(
                "https_allow_insecure", default=False,
                help="Whether to disable the validation of HTTPS "
                     "certificates."),
            cfg.StrOpt(
                "https_ca_bundle", default=None,
                help="The path to a CA_BUNDLE file or directory with "
                     "certificates of trusted CAs."),
        ]

    def register(self):
        """Register the current options to the global ConfigOpts object."""
        group = cfg.OptGroup(self.group_name, title='OracleCloud Options')
        self._config.register_group(group)
        self._config.register_opts(self._options, group=group)

    def list(self):
        """Return a list which contains all the available options."""
        return self._options
