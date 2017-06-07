import boto3
import datetime
import uuid
import os
import urllib
from django.http import JsonResponse

def sign_s3(request):
    print(request);
    S3_BUCKET = os.environ.get('S3_BUCKET')

    today = datetime.datetime.now()
    date_path = today.strftime("%Y/%m/%d")
    file_uuid = str(uuid.uuid4().hex)
    file_name = file_uuid + '-' + request.GET['file_name']
    full_path = os.path.join(date_path, file_name)

    file_type = request.GET['file_type']

    s3 = boto3.client('s3')
    presigned_post = s3.generate_presigned_post(
        Bucket = S3_BUCKET,
        Key = full_path,
        Fields = {"acl": "public-read", "Content-Type": file_type},
        Conditions = [
          {"acl": "public-read"},
          {"Content-Type": file_type}
        ],
        ExpiresIn = 3600
    )

    return JsonResponse({
        'data': presigned_post,
        'url': 'https://%s.s3.amazonaws.com/%s' % (S3_BUCKET, full_path)
    })
