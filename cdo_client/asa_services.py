from .base import CDOBaseClient
import logging

logger = logging.getLogger(__name__)


class CDOASAServices(CDOBaseClient):
    """Class for performing CDO ASA operations"""

    def __init__(self, api_token, region, api_version="", verify=""):
        super().__init__(api_token, region, api_version=api_version, verify=verify)
        self.service_prefix = f"/aegis/rest/v{self.api_version}/services"

    # TODO: Full CRUD operations where available
    # TODO: packettracer method(s)

    def get_asa_config_summary_list(self):
        return self.get_operation(f"{self.service_prefix}/asa/configs")

    def get_asa_config_summary(self, device_uid):
        return self.get_operation(f"{self.service_prefix}/asa/configs/{device_uid}")

    def get_asa_nats_list(self):
        return self.get_operation(f"{self.service_prefix}/asa/nats")

    def get_asa_nat(self, nat_uid):
        return self.get_operation(f"{self.service_prefix}/asa/nats/{nat_uid}")

    def get_asa_twice_nat_events_list(self):
        return self.get_operation(f"{self.service_prefix}/asa/twicenatevents")

    def get_asa_twice_nat_events(self, twice_nat_uid):
        return self.get_operation(f"{self.service_prefix}/asa/twicenatevents/{twice_nat_uid}")

    def get_asa_exports_list(self):
        return self.get_operation(f"{self.service_prefix}/asa/exports")

    def get_asa_exports(self, export_uid):
        return self.get_operation(f"{self.service_prefix}/asa/exports/{export_uid}")

    def get_asa_devices_configs_list(self):
        return self.get_operation(f"{self.service_prefix}/asa/devices-configs")

    def get_asa_devices_configs(self, devices_configs_uid):
        return self.get_operation(f"{self.service_prefix}/asa/devices-configs/{devices_configs_uid}")

    def get_asa_templates_list(self):
        return self.get_operation(f"{self.service_prefix}/asa/templates")

    def get_asa_templates(self, template_uid):
        return self.get_operation(f"{self.service_prefix}/asa/templates/{template_uid}")

    def get_asa_debug_events_list(self):
        return self.get_operation(f"{self.service_prefix}/asa/debugevents")

    def get_asa_debug_events(self, events_uid):
        return self.get_operation(f"{self.service_prefix}/asa/debugevents/{events_uid}")

    def get_asa_ordered_nats_list(self, params):
        return self.get_operation(f"{self.service_prefix}/asa/orderednats", params=params)

    def get_asa_ordered_nats(self, ordered_nats_uid, params):
        return self.get_operation(f"{self.service_prefix}/asa/orderednats/{ordered_nats_uid}", params=params)

    def get_asa_configs_exports_list(self):
        return self.get_operation(f"{self.service_prefix}/asa/configs-exports")

    def get_asa_configs_exports(self, configs_exports_uid):
        return self.get_operation(f"{self.service_prefix}/asa/configs-exports/{configs_exports_uid}")

    def get_asa_nat_events_list(self):
        return self.get_operation(f"{self.service_prefix}/asa/natevents")

    def get_asa_nat_events(self, nat_events_uid):
        return self.get_operation(f"{self.service_prefix}/asa/natevents/{nat_events_uid}")
