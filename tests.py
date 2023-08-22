import requests as req

requests_ = [
    {},
    {'phoneNumber':123456},
    {'phoneNumber':12},
    {'email':'george@hillvalley.edu'},
    {'email':'absasdas'},
    {'email':'abs@ff.com'},
    {'phoneNumber':98712,'email':'abs@f'},
    {'phoneNumber':54321,'email':'newmail@mail.com'},
    {'phoneNumber':123456,'email':'email@mas.in'},
    {'phoneNumber':647384,'email':'email@mas.in'},
    {'phoneNumber':434343,'email':'george@hillvalley.edu'},
    {'phoneNumber':123456,'email':'mcfly@hillvalley.edu'},
    {'phoneNumber':647384,'email':'mcfly@hillvalley.edu'},
    {'phoneNumber':123456,'email':'george@hillvalley.edu'},
    {'phoneNumber':1,'email':'1@mail.com'},
    {'phoneNumber':2,'email':'2@mail.com'},
    {'phoneNumber':3,'email':'3@mail.com'},
    {'phoneNumber':4,'email':'4@mail.com'},
    {'phoneNumber':1,'email':'4@mail.com'},
    {'phoneNumber':2,'email':'3@mail.com'},
    {'phoneNumber':1,'email':'3@mail.com'},

]

for data in requests_:
    res = req.post('http://127.0.0.1:8000/identify',json=data)
    print('data:',data,'\n','result:',res,res.text,'\n')
    input('press ENTER to continue')
