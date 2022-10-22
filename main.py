import asyncio
import logging

from th_sensor_reader.scanner import scan


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)-15s %(name)-8s %(levelname)s: %(message)s",
    )
    try:
        asyncio.run(scan())
    except KeyboardInterrupt:
        pass
