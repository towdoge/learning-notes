# 生产者代码
import pika

#
#
credentials = pika.PlainCredentials('atl-aps', 'atl-aps')  # mq用户名和密码，没有则需要自己创建
# 虚拟队列需要指定参数 virtual_host，如果是默认的可以不填。
connection = pika.BlockingConnection(pika.ConnectionParameters(host='10.7.71.112',
                                                               port=5672,
                                                               virtual_host='algorithm',
                                                               credentials=credentials))
queue_name = 'algorithm_call_queue_112'
# 建立rabbit协议的通道
channel = connection.channel()
# 声明消息队列，消息将在这个队列传递，如不存在，则创建。durable指定队列是否持久化
channel.queue_declare(queue=queue_name, durable=True)

# message不能直接发送给queue，需经exchange到达queue，此处使用以空字符串标识的默认的exchange
# 向队列插入数值 routing_key是队列名
channel.basic_publish(exchange='algorithm_direct',
                      routing_key='10.7.71.112',
                      body='Hello world！1')

# 关闭与rabbitmq server的连接
connection.close()
