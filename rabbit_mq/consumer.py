# 消费者代码
import pika

credentials = pika.PlainCredentials('atl-aps', 'atl-aps')
# BlockingConnection:同步模式
connection = pika.BlockingConnection(pika.ConnectionParameters(host='10.7.71.112',
                                                               port=5672,
                                                               virtual_host='algorithm',
                                                               credentials=credentials))
channel = connection.channel()
queue_name = 'algorithm_call_queue_113'
# 申明消息队列。当不确定生产者和消费者哪个先启动时，可以两边重复声明消息队列。
channel.queue_declare(queue=queue_name, durable=True)


# 定义一个回调函数来处理消息队列中的消息，这里是打印出来
def callback(ch, method, properties, body):
    print(body.decode())
    # 告诉生产者，消费者已收到消息
    # 手动发送确认消息
    ch.basic_ack(delivery_tag=method.delivery_tag)



channel.queue_bind(exchange='algorithm_direct', queue=queue_name,
                   routing_key='10.7.71.113')
# 告诉rabbitmq，用callback来接收消息
# 默认情况下是要对消息进行确认的，以防止消息丢失。
# 此处将auto_ack明确指明为True，不对消息进行确认。
channel.basic_consume(queue=queue_name,
                      on_message_callback=callback)
                    # auto_ack=True)  # 自动发送确认消息
# 开始接收信息，并进入阻塞状态，队列里有信息才会调用callback进行处理
channel.start_consuming()
