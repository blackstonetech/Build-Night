import boto3, sys


s = boto3.client('sns', region_name='us-east-1')
s.publish(Message='Current Score: '+ str(sys.argv[1]), PhoneNumber='+13015025813')
