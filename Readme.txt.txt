1. make an account on heroku
2. install heroku cli
3. after installing cli, 
>>  heroku login
>> heroku create
>> >heroku apps:rename newname--app oldname

we want to use node as well as python.
>> heroku buildpacks:set heroku/python --app <<appname>>
>> heroku buildpacks:add --index 1 heroku/nodejs --app <<appname>>			//use nodejs at first position. so now python is at 

View buildpacks

>> heroku buildpacks

add  node version to package.json
  "engines": {
    "node": "8.x"
  }

make a requirements.txt file in root folder
