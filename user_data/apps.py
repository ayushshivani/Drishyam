from django.apps import AppConfig
import pandas as pd
import os

class UserDataConfig(AppConfig):
    name = 'prediction'
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
