import MetaTrader5 as mt5

def initialize_mt5_connection(conexion_mt5):
    mt5.initialize(
        path=conexion_mt5['path'],
        login=conexion_mt5['login'],
        password=conexion_mt5['password'],
        server=conexion_mt5['server'],
        timeout=conexion_mt5['timeout'],
        portable=conexion_mt5['portable']
    )

def shutdown_mt5_connection():
    mt5.shutdown()
