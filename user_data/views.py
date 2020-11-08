from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from user_data.apps import UserDataConfig
import json
import hashlib


count = 0

class UserDataEntry(APIView):


    def __init__(self):
        super().__init__()

    def post(self, request, format=None):
        global count
        data = request.data
        secret_key = data['secret_key']
        description = data['data']
        file_data = {"secret_key":secret_key,"data":description}
        file_data = json.dumps(file_data)
        file_data.encode('utf-8')

        file_name = 'files/file_' + str(count) + '.txt'
        count += 1
        f = open(file_name,"a")
        f.write(file_data)
        f.close()
        
        md5_returned = hashlib.md5(file_data.encode()).hexdigest()
        response_dict = {"MD5sum": md5_returned}
        return Response(response_dict, status=200)