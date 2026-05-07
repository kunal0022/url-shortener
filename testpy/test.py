# import boto3

# ec2 = boto3.client('ec2')
# isinstance = ec2.describe_instances()


###list --- its mutable 
a = [1,2,3]
a.append(4)
print(a)
###tuple --- its immutable
b = (1,2,3)
#b.append(-1)
print(b)
## Output:[1, 2, 3, 4]
## Output:AttributeError: 'tuple' object has no attribute 'append'
# set --- its mutable but it does not allow duplicates
c = {1,2,3}
c.add(4)
c.add(2)
print(c)
## Output:{1, 2, 3, 4}

#dict --- its mutable and it has key value pairs
d = {'a':1, 'b':2}
d['c'] = 3
print(d)
## Output:{'a': 1, 'b': 2, 'c': 3}

print(d ['a'])
print(d.get('b'))

