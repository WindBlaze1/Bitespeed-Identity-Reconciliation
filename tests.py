import requests as req

requests_ = [
    {},
    {'phoneNumber':123456},
    {'phoneNumber':12},
    {'email':'george@hillvalley.edu'},
    {'email':'absasdas'},
    {'email':'abs@ff.com'},
    {'phoneNumber':54321,'email':'newmail@mail.com'},
    {'phoneNumber':123456,'email':'email@mas.in'},
    {'phoneNumber':647384,'email':'email@mas.in'},
    {'phoneNumber':434343,'email':'george@hillvalley.edu'},
    {'phoneNumber':123456,'email':'mcfly@hillvalley.edu'},
    {'phoneNumber':647384,'email':'mcfly@hillvalley.edu'},
    {'phoneNumber':123456,'email':'george@hillvalley.edu'},
]

for data in requests_:
    res = req.post('https://bitespeed-assignment-harit.onrender.com/identify',json=data)
    print('data:',data,'\n','result:',res,res.text,'\n')
    input('press ENTER to continue')
