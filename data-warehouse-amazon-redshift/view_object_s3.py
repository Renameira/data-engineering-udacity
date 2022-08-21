import boto3
from config import Settings

prefix = "song_data"

def view_object_in_bucket_public():
    s3 = boto3.resource(
        "s3",
        region_name=Settings.REGION,
        aws_access_key_id=Settings.KEY,
        aws_secret_access_key=Settings.SECRET,
        aws_session_token=Settings.TOKEN,
    )

    sampleDbBucket = s3.Bucket("udacity-dend")

    for obj in sampleDbBucket.objects.filter(Prefix=prefix):
        print(obj)


if __name__ == "__main__":
    view_object_in_bucket_public()
