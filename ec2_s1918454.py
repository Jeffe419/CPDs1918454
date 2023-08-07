import boto3

ec2 = boto3.resource('ec2')

# creating the ec2 instance
instances = ec2.create_instances(
     ImageId='ami-04823729c75214919',
     MinCount=1,
     MaxCount=1,
     InstanceType='t2.micro',
     KeyName='jeff-s1918454'  
 )
