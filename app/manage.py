from app import create_app

server = flask.Flask(__name__)
if __name__ == '__main__':
 #port可以指定端口，默认端口是5000
 #host写成0.0.0.0的话，其他人可以访问，代表监听多块网卡上面，默认是127.0.0.1
    create_database()       #创建数据库
    create_table()          #创建表
    server.run(debug=True, port=8899, host='0.0.0.0')
