import json, os
from flask import Flask, redirect, request, url_for
from flask_login import LoginManager, current_user, login_manager,login_user,logout_user

from oauthlib.oauth2 import WebApplicationClient
import requests

from model import init_db_command
from user import User