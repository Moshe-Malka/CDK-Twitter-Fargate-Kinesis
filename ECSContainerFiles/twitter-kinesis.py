from tweepy.streaming import StreamListener
from tweepy import OAuthHandler, Stream
import os, json, sys
import boto3

# aws secretsmanager create-secret --name TwitterAPISecrets --secret-string file://twitter_credentials.json
KINESIS_STREAM_NAME = os.environ.get('KINESIS_STREAM_NAME', 'twitter-stream')
REGION_NAME = os.environ.get('REGION_NAME', 'eu-west-1')
KEYWORD = os.environ.get('KEYWORD')
SECRETS_NAME = os.environ.get('SECRETS_NAME')

session = boto3.session.Session(region_name=REGION_NAME)
secretsmanager_client = session.client(service_name='secretsmanager', region_name=REGION_NAME)

class MyStreamListener(StreamListener):
    def __init__(self):
        self.kinesis_client = session.client('kinesis')
        print('[*] Starting Stream...')

    def on_data(self, data):
        self.put_record(json.loads(data))
        return True
    
    def put_record(self, data):
        try:
            response = self.kinesis_client.put_record(
                StreamName=KINESIS_STREAM_NAME,
                Data=json.dumps(data),
                PartitionKey=data.get('id_str') if data.get('id_str') else str(data.get('id')) 
            )
        except Exception as e:
            print(f"Error while trying to put a record - {e}")

    def on_error(self, status_code):
        print(f"[*] Error : {status_code}")
        if status_code == 420:
            print("[*] Disconnecting Stream...")
            #returning False in on_error disconnects the stream
            return False
        else:
            print("[*] Reconnecting Stream...")
            return True

def get_secret(secret_name):
    try:
        secret_value = secretsmanager_client.get_secret_value( SecretId=secret_name )
        return json.loads(secret_value['SecretString'])
    except ClientError as e:
        print(e)

if __name__ == '__main__':
    # Auth
    try:
        creds = get_secret(SECRETS_NAME)
        auth = OAuthHandler(creds['API_KEY'], creds['API_SECRET_KEY'])
        auth.set_access_token(creds['ACCESS_TOKEN'], creds['ACCESS_TOKEN_SECRET'])
    except Exception as e:
        print(f"Failed to authinticate - {e}")
    
    # Stream initialization
    try:
        stream = Stream(auth, MyStreamListener())
        stream.filter(track=[KEYWORD])
    except KeyboardInterrupt:
        print(f"\n[*] Keyboard Interrupt")
        stream.disconnect()
    except Exception as e:
        print(f"Streaming Failed - {e}")
    
