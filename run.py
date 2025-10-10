import os
from app import create_app
from dotenv import load_dotenv, dotenv_values 

load_dotenv()
env = os.getenv('FLASK_ENV')

config_map = {
    'development': ('development', 'config.DevelopmentConfig'),
    'testing': ('testing', 'config.TestingConfig'),
    'production': ('production', 'config.ProductionConfig'),
    }

app_env = config_map.get(env, config_map['production'])
print('-----------------------------------------')
print(f'Environment configured for {app_env[0]}')
print('_________________________________________')

app = create_app(app_env[1])

if __name__ == '__main__':
    app.run()
