ARG BUILD_FROM
FROM ${BUILD_FROM}

ENV DEBIAN_FRONTEND=noninteractive
ENV LANG=C.UTF-8

RUN apk add --no-cache \
  python3 \
  py3-pip \
  glib \
  mesa-gl

RUN pip3 install --no-cache-dir \
  numpy \
  opencv-python-headless \
  mediapipe

WORKDIR /app

COPY rootfs/ /

CMD [ "/run.sh" ]
