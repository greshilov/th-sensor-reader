

FROM python:3.10

WORKDIR /app
ENV BLUEZ_VERSION 5.65

RUN apt-get update && apt-get install -y wget libdbus-1-dev libudev-dev libical-dev udev

RUN wget http://www.kernel.org/pub/linux/bluetooth/bluez-$BLUEZ_VERSION.tar.xz && \
    tar -xvf bluez-$BLUEZ_VERSION.tar.xz && \
    cd bluez-$BLUEZ_VERSION/ && \
    ./configure --prefix=/usr     \
            --sysconfdir=/etc     \
            --localstatedir=/var  \
            --enable-library      \
            --disable-manpages    \
            --disable-systemd     && \
    make install && \
    ln -svf ../libexec/bluetooth/bluetoothd /usr/sbin

COPY ./etc/init.d/bluetooth /etc/init.d/bluetooth

COPY requirements.txt .
RUN pip install -r requirements.txt

ADD th_sensor_reader ./th_sensor_reader
COPY main.py entrypoint.sh ./

CMD ["bash", "entrypoint.sh"]
