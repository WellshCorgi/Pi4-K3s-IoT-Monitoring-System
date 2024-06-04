const amqp = require('amqplib/callback_api');

let latestMessage = null;

const connectRabbitMQ = (callback) => {
    const rabbitmqUrl = 'amqp://bochan:bochan@localhost:5672';

    amqp.connect(rabbitmqUrl, (err, connection) => {
        if (err) {
            console.error('RabbitMQ 연결 실패', err);
            process.exit(1);
        }

        connection.createChannel((err, channel) => {
            if (err) {
                console.error('RabbitMQ 채널 생성 실패', err);
                process.exit(1);
            }

            const exchange = 'cpu-data-exchange';
            const queue = 'stream_queue';
            const routingKey = 'info';

            channel.assertExchange(exchange, 'direct', { durable: false });
            channel.assertQueue(queue, { durable: false });
            channel.bindQueue(queue, exchange, routingKey);

            channel.consume(queue, (msg) => {
                if (msg.content) {
                    latestMessage = msg.content.toString();
                    console.log("메시지 수신:", latestMessage);
                }
            }, { noAck: true });

            callback();
        });
    });
};

const getLatestInfo = () => {
    if (latestMessage) {
        try {
            return JSON.parse(latestMessage);
        } catch (error) {
            console.error('메시지 파싱 실패', error);
            return null;
        }
    } else {
        return null;
    }
};

module.exports = {
    connectRabbitMQ,
    getLatestInfo
};
