# author: wr786
from flask import Flask, session, render_template, request, redirect, send_from_directory
import hashlib
import sqlalchemy

app = Flask(__name__)

