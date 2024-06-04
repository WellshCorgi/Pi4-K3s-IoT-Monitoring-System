# Telegraf Docker Setup

This guide will help you set up Telegraf using Docker with a provided configuration file.

## Prerequisites

- Docker installed on your system
- Telegraf configuration file (`telegraf.conf`)

## Configuration

Ensure that your `telegraf.conf` file is in the current directory (`$PWD`). This file contains the necessary settings for Telegraf, including the token for authentication.


## Command for Running

(`docker run -d --name=telegraf  --network=host  -v $PWD/telegraf.conf:/etc/telegraf/telegraf.conf:ro telegraf`)

### Sample Configuration

Here is a snippet of what your `telegraf.conf` might look like:

```toml
# Telegraf Configuration
[[outputs.influxdb_v2]]
  token = "put your token"
  ...
