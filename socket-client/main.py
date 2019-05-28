from Client import Client
import global_var
if __name__ == '__main__':
    ip = str(input('Which ip : '))
    client_server_ip = Client(ip, 'server_ip_connection')

    client_server_ip.start()
    client_server_ip.join()
    node_ip = client_server_ip.get_node_ip()
    global_var.server.start(node_ip, 8000)
