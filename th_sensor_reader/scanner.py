import asyncio
import logging

from bleak import BleakScanner
from bleak.backends.bluezdbus.advertisement_monitor import (
    AdvertisementDataType,
    OrPattern,
)
from bleak.backends.bluezdbus.scanner import BlueZScannerArgs

from influxdb_client import InfluxDBClient

from .config import USERNAME, PASSWORD
from .data_reader import DataReader

logger = logging.getLogger(__name__)


async def scan():
    influx_client = InfluxDBClient(
        url="http://localhost:8086",
        token=f"{USERNAME}:{PASSWORD}",
        org="-",
    )

    reader = DataReader(
        address="58:2D:34:10:FE:D1",
        target_service="0000fdcd-0000-1000-8000-00805f9b34fb",
        influx_client=influx_client,
    )

    while True:
        async with BleakScanner(
            detection_callback=reader.read_data,
            #scanning_mode="passive",
            #bluez=BlueZScannerArgs(
            #    or_patterns=[
            #        OrPattern(0, AdvertisementDataType.FLAGS, b"\x06"),
            #    ]
            #),
        ) as scanner:
            await asyncio.sleep(30)
