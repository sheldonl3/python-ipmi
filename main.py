import pyipmi
import pyipmi.interfaces

# Supported interface_types for ipmitool are: 'lan' , 'lanplus', and 'serial-terminal'
interface = pyipmi.interfaces.create_interface('ipmitool', interface_type='lanplus')

connection = pyipmi.create_connection(interface)

connection.target = pyipmi.Target(0x20)

connection.session.set_session_type_rmcp('127.0.0.1', port=12345)
connection.session.set_auth_type_user('root', '0penBmc')
connection.session.establish()

#status = connection.set_username(2,'misaka')
status = connection.get_username(2)
print(status)