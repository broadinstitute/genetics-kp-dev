#!/usr/bin/env python3

import connexion
import os
from openapi_server import encoder

# def main():
#     app = connexion.App(__name__, specification_dir='./openapi/')
#     app.app.json_encoder = encoder.JSONEncoder
#     app.add_api('openapi.yaml',
#                 arguments={'title': 'Genetics Data Provider for NCATS Biomedical Translator Reasoners'},
#                 pythonic_params=True)

#     # config
#     network_port = os.environ.get('PORT')

#     # app.run(port=8080)
#     # app.run(port=7002)
#     app.run(port=network_port)


app = connexion.App(__name__, specification_dir='./openapi/')
app.app.json_encoder = encoder.JSONEncoder
app.add_api('openapi.yaml',
            arguments={'title': 'Molecular Data Provider for NCATS Biomedical Translator'},
            pythonic_params=True)

def main():
    # config
    network_port = os.environ.get('PORT')
    app.run(port=network_port)


if __name__ == '__main__':
    main()
