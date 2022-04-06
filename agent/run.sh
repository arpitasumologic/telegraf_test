#!/bin/bash
usage() {
  echo "Usage: $0 [ -c config-file-path ]" 1>&2
  exit 0
}
CONFIG_FILE="config.txt"
while getopts ":h:c:" options; do
  case "${options}" in
  c)
    CONFIG_FILE=${OPTARG}
    echo ${CONFIG_FILE}
    ;;
  h)
    usage
    ;;
  *)
    usage
    ;;
  esac
done

while IFS= read -r line; do
  line=$(echo $line)
  if [[ "$line" =~ ^[[:digit:]] ]]; then
    tokens=($line)
    PORT="${tokens[0]}"
    EXPORT_FORMAT="${tokens[1]}"
    URL="${tokens[2]}"
    ID=$(
      docker container ls --format="{{.ID}}\t{{.Ports}}" |
        grep "0.0.0.0:${PORT}" |
        awk '{print $1}'
    )
    if [ ! -z "$ID" ]; then
      echo "Stopping and removing Container ID: ${ID}"
      docker container stop ${ID} && docker container rm -f ${ID}
    fi
    echo "Running docker on port: ${PORT}"
    docker run -d -e URL="${URL}" -e EXPORT_FORMAT="${EXPORT_FORMAT}" -v $(pwd)/telegraf.conf:/etc/telegraf/telegraf.conf:ro \
      --add-host=host.docker.internal:host-gateway -p ${PORT}:8092/udp telegraf \
      --config /etc/telegraf/telegraf.conf
  fi
done <"${CONFIG_FILE}"
docker container ls --no-trunc | grep telegraf
