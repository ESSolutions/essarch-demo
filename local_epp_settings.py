import os
# Default values which can be overridden by setting the environment variables
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_PORT = os.environ.get('DB_PORT', '3003')
ELASTICSEARCH_HOST = os.environ.get('ELASTICSEARCH_HOST', 'localhost')
ELASTICSEARCH_PORT = os.environ.get('ELASTICSEARCH_PORT', '9200')
LOGSTASH_HOST = os.environ.get('LOGSTASH_HOST', 'localhost')
LOGSTASH_PORT = os.environ.get('LOGSTASH_PORT', '5003')
REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
REDIS_PORT = os.environ.get('REDIS_PORT', '6003')
REDIS_CONTEXT = os.environ.get('REDIS_CONTEXT', '/3')
RABBITMQ_HOST = os.environ.get('RABBITMQ_HOST', 'localhost')
RABBITMQ_PORT = os.environ.get('RABBITMQ_PORT', '15003')
RABBITMQ_CONTEXT = os.environ.get('RABBITMQ_CONTEXT', '/epp')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'epp',
        'USER': 'arkiv',
        'PASSWORD': 'password',
        'HOST': DB_HOST,
        'PORT': DB_PORT,
        'OPTIONS': {
            'isolation_level': 'read committed',
        }
    }
}

ELASTICSEARCH_CONNECTIONS = {
    'default': {
        'hosts': [{
            'host': ELASTICSEARCH_HOST,
            'port': ELASTICSEARCH_PORT,
            'timeout': 60,
        }],
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s %(levelname)s %(message)s'
        },
        'logstash': {
            '()': 'logstash_async.formatter.DjangoLogstashFormatter',
            'message_type': 'logstash',
            'fqdn': False,
            'extra_prefix': '',
            'extra': {
                'application': 'EPP',
                'environment': 'dev'
            }
        },
        'logstash_http': {
            '()': 'logstash_async.formatter.DjangoLogstashFormatter',
            'message_type': 'django_http',
            'fqdn': False,
            'extra_prefix': '',
            'extra': {
                'application': 'EPP',
                'environment': 'dev'
            }
        },
    },
    'handlers': {
        'core': {
            'level': 'DEBUG',
            'class': 'ESSArch_Core.log.dbhandler.DBHandler',
            'application': 'ESSArch Preservation Platform',
            'agent_role': 'Archivist',
        },
        'file_epp': {
            'level': 'DEBUG',
            'formatter': 'verbose',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/ESSArch/log/epp.log',
            'maxBytes': 1024 * 1024 * 100,  # 100MB
            'backupCount': 5,
        },
        'log_file_auth': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'verbose',
            'filename': '/ESSArch/log/auth_epp.log',
            'maxBytes': 1024 * 1024 * 100,  # 100MB
            'backupCount': 5,
        },
        'logstash_http': {
            'level': 'INFO',
            'class': 'logstash_async.handler.AsynchronousLogstashHandler',
            'formatter': 'logstash_http',
            'transport': 'logstash_async.transport.TcpTransport',
            'host': LOGSTASH_HOST,
            'port': int(LOGSTASH_PORT),
            'ssl_enable': False,
            'ssl_verify': False,
            'ca_certs': 'etc/ssl/certs/logstash_ca.crt',
            'certfile': '/etc/ssl/certs/logstash.crt',
            'keyfile': '/etc/ssl/private/logstash.key',
            'database_path': '{}/epp_logstash_http.db'.format('/var/tmp'),
        },
        'logstash': {
            'level': 'INFO',
            'class': 'logstash_async.handler.AsynchronousLogstashHandler',
            'formatter': 'logstash',
            'transport': 'logstash_async.transport.TcpTransport',
            'host': LOGSTASH_HOST,
            'port': int(LOGSTASH_PORT),
            'ssl_enable': False,
            'ssl_verify': False,
            'ca_certs': 'etc/ssl/certs/logstash_ca.crt',
            'certfile': '/etc/ssl/certs/logstash.crt',
            'keyfile': '/etc/ssl/private/logstash.key',
            'database_path': '{}/epp_logstash.db'.format('/var/tmp'),
        },
    },
    'loggers': {
        'essarch': {
            'handlers': ['core', 'file_epp', 'logstash'],
            'level': 'INFO',
        },
        'essarch.auth': {
            'level': 'INFO',
            'handlers': ['log_file_auth', 'logstash'],
            'propagate': False,
        },
        'django': {
            'handlers': ['logstash'],
            'level': 'INFO',
        },
        'django.request': {
            'handlers': ['logstash'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.security': {
            'handlers': ['logstash'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.channels.server': {
            'handlers': ['logstash_http'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.contrib.auth': {
            'handlers': ['logstash'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

REDIS_ADDR = f'redis://{REDIS_HOST}:{REDIS_PORT}{REDIS_CONTEXT}'

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [REDIS_ADDR],
        },
    },
}

CACHES = {
    'default': {
        'TIMEOUT': None,
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': REDIS_ADDR,
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

RABBITMQ_URL = f'amqp://rabbitmq:rabbitmq@{RABBITMQ_HOST}:{RABBITMQ_PORT}{RABBITMQ_CONTEXT}'
CELERY_RESULT_BACKEND = REDIS_ADDR
