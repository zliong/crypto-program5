from flask import Flask, render_template, request, redirect, url_for, flash
import boto3
import boto
from boto3.dynamodb.conditions import Key
from botocore.client import ClientError
from urllib.request import urlopen
import urllib3
import codecs

application = Flask(__name__)


@application.route('/')
def home_page():
    return render_template("base.html")


if __name__ == "__main__":
    application.run()