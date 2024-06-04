import pika
import psutil
import json
import time

def connect_rabbitmq():
    '''
    RabbitMQ 연결 설정
    '''
    credentials = pika.PlainCredentials('bochan', 'bochan')
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', 5672, '/', credentials))
    channel = connection.channel()
    return connection, channel

def get_system_info(endpoint):
    '''
    CPU 사용률 및 RAM 정보 수집 후, Influx Line Protocol 형식으로 변환
    '''
    cpu_percent = psutil.cpu_percent(interval=1)
    ram_info = psutil.virtual_memory()
    
    if endpoint == 'influxDB':
        influx_data = f"system_info cpu_percent={cpu_percent},ram_total={ram_info.total},ram_used={ram_info.used},ram_free={ram_info.free}"
        
        return influx_data
    elif endpoint == 'API':
        resource_data = {
        "cpu_percent": cpu_percent,
        "ram_total": ram_info.total,
        "ram_used": ram_info.used,
        "ram_free": ram_info.free
        }
        return json.dumps(resource_data)
        


def send_data(channel, exchange, routing_key, data):
    '''
    데이터를 RabbitMQ로 전송
    '''
    channel.basic_publish(exchange=exchange, routing_key=routing_key, body=data)
    print(f"System info sent to RabbitMQ : {data}")

def main():
    connection, channel = connect_rabbitmq()
    try:
        while True:
            influx_data = get_system_info('influxDB')
            stream_data = get_system_info('API')

            # 데이터 전송
            send_data(channel, 'edge-resource-exchange', 'info', influx_data)
            send_data(channel, 'cpu-data-exchange', 'info', stream_data)

            time.sleep(1)
    except KeyboardInterrupt:
        print("Interrupted by user")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        connection.close()
        print("Connection closed")

if __name__ == "__main__":
    main()
