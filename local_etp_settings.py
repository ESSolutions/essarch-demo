import os
# Default values which can be overridden by setting the environment variables
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_PORT = os.environ.get('DB_PORT', '3001')
ELASTICSEARCH_HOST = os.environ.get('ELASTICSEARCH_HOST', 'localhost')
ELASTICSEARCH_PORT = os.environ.get('ELASTICSEARCH_PORT', '9200')
LOGSTASH_HOST = os.environ.get('LOGSTASH_HOST', 'localhost')
LOGSTASH_PORT = os.environ.get('LOGSTASH_PORT', '5001')
REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
REDIS_PORT = os.environ.get('REDIS_PORT', '6001')
RABBITMQ_HOST = os.environ.get('RABBITMQ_HOST', 'localhost')
RABBITMQ_PORT = os.environ.get('RABBITMQ_PORT', '15001')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'etp',
        'USER': 'arkiv',
        'PASSWORD': 'password',
        'HOST': DB_HOST,
        'PORT': DB_PORT,
        'OPTIONS': {
            'isolation_level': 'read committed',
        }
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
                'application': 'ETP',
                'environment': 'dev'
            }
        },
        'logstash_http': {
            '()': 'logstash_async.formatter.DjangoLogstashFormatter',
            'message_type': 'django_http',
            'fqdn': False,
            'extra_prefix': '',
            'extra': {
                'application': 'ETP',
                'environment': 'dev'
            }
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
        'core': {
            'level': 'DEBUG',
            'class': 'ESSArch_Core.log.dbhandler.DBHandler',
            'application': 'ESSArch Tools for Producer',
            'agent_role': 'Producer',
        },
        'file_etp': {
            'level': 'DEBUG',
            'formatter': 'verbose',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/ESSArch/log/etp.log',
            'maxBytes': 1024 * 1024 * 100,  # 100MB
            'backupCount': 5,
        },
        'log_file_auth': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'verbose',
            'filename': '/ESSArch/log/auth_etp.log',
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
            'database_path': '{}/etp_logstash_http.db'.format('/var/tmp'),
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
            'database_path': '{}/etp_logstash.db'.format('/var/tmp'),
        },
    },
    'loggers': {
        'essarch': {
            'handlers': ['core', 'file_etp', 'logstash'],
            'level': 'DEBUG',
        },
        'essarch.auth': {
            'level': 'INFO',
            'handlers': ['log_file_auth', 'logstash'],
            'propagate': False,
        },
        'django': {
            'handlers': ['logstash', 'console'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['logstash'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.security': {
            'handlers': ['logstash'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'django.channels.server': {
            'handlers': ['logstash_http', 'console'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.contrib.auth': {
            'handlers': ['logstash'],
            'level': 'INFO',
            'propagate': False,
        },
    }
}

REDIS_ADDR = f'redis://{REDIS_HOST}:{REDIS_PORT}'

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

RABBITMQ_URL = f'amqp://rabbitmq:rabbitmq@{RABBITMQ_HOST}:{RABBITMQ_PORT}'
CELERY_RESULT_BACKEND = REDIS_ADDR
