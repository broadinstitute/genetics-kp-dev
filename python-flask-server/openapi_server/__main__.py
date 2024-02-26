#!/usr/bin/env python3

import connexion
import os 

from openapi_server import encoder
from openapi_server.dcc.utils import get_logger

# get logger
logger = get_logger(__name__)

# check to make sure dev flag is not on (jaegger not loaded if on)
IS_DEV = False
ENV_IS_DEV = os.environ.get('IS_DEV')
if ENV_IS_DEV:
    IS_DEV = True
logger.info('IS_DEV flag set to {}'.format(IS_DEV))

# import open telemetry
try:
    from opentelemetry.instrumentation.flask import FlaskInstrumentor
    from opentelemetry import trace
    from opentelemetry.sdk.resources import SERVICE_NAME as telemetery_service_name_key, Resource
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor
    from opentelemetry.exporter.jaeger.thrift import JaegerExporter
    from opentelemetry.instrumentation.requests import RequestsInstrumentor
    # from opentelemetry.instrumentation.pymysql import PyMySQLInstrumentor
    OTEL_ENABLED = True
    logger.info("OPENTELEMETRY imported; OTEL_ENABLED set to: {}".format(OTEL_ENABLED))
except ImportError:
    OTEL_ENABLED = False
    logger.info("OPENTELEMETRY import FAILED; OTEL_ENABLED set to: {}".format(OTEL_ENABLED))


# def main():
#     app = connexion.App(__name__, specification_dir='./openapi/')
#     app.app.json_encoder = encoder.JSONEncoder
#     app.add_api('openapi.yaml',
#                 arguments={'title': 'Genetics Data Provider for NCATS Biomedical Translator Reasoners'},
#                 pythonic_params=True)

#     app.run(port=8080)


app = connexion.App(__name__, specification_dir='./openapi/')
app.app.json_encoder = encoder.JSONEncoder
app.add_api('openapi.yaml',
            arguments={'title': 'Genetics Data Provider for NCATS Biomedical Translator Reasoners'},
            pythonic_params=True)

def load_otel(otel_enabled=False):
    if otel_enabled:
        logger.info('About to instrument app for OTEL')

        # set the service name for our trace provider
        otel_service_name = 'genetics-data-provider'
        tp = TracerProvider(
                resource=Resource.create({telemetery_service_name_key: otel_service_name})
            )
        # create an exporter to jaeger
        jaeger_host = 'jaeger-otel-agent.sri'
        jaeger_port = 6831
        jaeger_exporter = JaegerExporter(
                    agent_host_name=jaeger_host,
                    agent_port=jaeger_port,
                )
        # here we use the exporter to export each span in a trace
        tp.add_span_processor(
            BatchSpanProcessor(jaeger_exporter)
        )
        trace.set_tracer_provider(
            tp
        )
        otel_excluded_urls = 'health,api/health,api/dev/.*'
        FlaskInstrumentor().instrument_app(app.app, excluded_urls=otel_excluded_urls)
        RequestsInstrumentor().instrument()
        logger.info('Finished instrumenting app for OTEL')

def main():
    # start open telemetry
    print("in main(), IS_DEV set to: {}".format(IS_DEV))
    if not IS_DEV:
        logger.info("initializing opentelemetry with OTEL_ENABLED set to: {}".format(OTEL_ENABLED))
        load_otel(otel_enabled=OTEL_ENABLED)

    # config
    network_port = os.environ.get('FLASK_PORT')
    app.run(port=network_port)





if __name__ == '__main__':
    main()

