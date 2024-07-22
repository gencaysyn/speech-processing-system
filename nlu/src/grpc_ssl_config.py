import logging

import grpc


def get_ssl_server_credentials():
    try:
        server_key = open('../ssl/server.key', 'rb').read()
        server_cert = open('../ssl/server.cert', 'rb').read()
        ca_cert = open('../ssl/ca.cert', 'rb').read()

        return grpc.ssl_server_credentials(
            [(server_key, server_cert)],
            root_certificates=ca_cert,
            require_client_auth=True
        )
    except FileNotFoundError as e:
        logging.exception("File not found!", exc_info=e)
        raise

