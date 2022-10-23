import dataclasses
import logging

from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData

from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS

from .config import BUCKET

logger = logging.getLogger(__name__)


@dataclasses.dataclass
class TData:
    temperature: float
    humidity: float  # percent
    battery: int  # percent

    @classmethod
    def from_bytes(cls, data: bytes) -> "TData":
        temperature = int.from_bytes(data[10:12], "little") / 10
        humidity = int.from_bytes(data[12:14], "little") / 10
        battery = data[-1]

        return TData(
            temperature=temperature,
            humidity=humidity,
            battery=battery,
        )


class DataReader:
    def __init__(
        self, address: str, target_service: str, influx_client: InfluxDBClient
    ):
        self.address = address
        self.target_service = target_service
        self.last_data = None
        self.influx_client = influx_client

    def read_data(self, device: BLEDevice, advertisement_data: AdvertisementData):
        logger.debug(f"{device.address} RSSI: {device.rssi}, {advertisement_data}")

        if (
            device.address == self.address
            and (data := advertisement_data.service_data.get(self.target_service))
            and data != self.last_data
        ):
            tdata = TData.from_bytes(data)
            self.write_to_db(tdata)
            self.last_data = data

    def write_to_db(self, tdata: TData):
        logger.info(f"writing data to a database: %r", tdata)

        write_api = self.influx_client.write_api(write_options=SYNCHRONOUS)

        write_api.write(
            bucket=BUCKET,
            record=tdata,
            record_measurement_name="tdata",
            record_field_keys=["temperature", "humidity", "battery"],
        )
