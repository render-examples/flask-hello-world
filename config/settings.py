roles=('Admin','Viewer')

# adding user for static login dictionary has been created down
user_dict={}
user_dict['amit@mail.com']={"id":"1","name":"Amit","password":"mypass"}
user_dict['suraj@mail.com']={"id":"2","name":"Suraj","password":"pass2"}
user_dict['amit@mail.com']['role']=roles[1]
user_dict['suraj@mail.com']['role']=roles[0]

category=[]
posts=[]