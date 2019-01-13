const express = require('express');
var app = express();
var upload = require('express-fileupload');
var bodyParser = require('body-parser');

// in latest body-parser use like below.
app.use(bodyParser.urlencoded({ extended: true }))
app.use(bodyParser.json());
app.use(bodyParser());

app.use(upload()); // configure middleware

app.get('/',function(req,res){
  res.sendFile(__dirname+'/index.html');
})

app.post('/upload',function(req,res){
  //console.log(req.files);
  if(req.files.upfile){
    var file = req.files.upfile,
      name = file.name,
      filename = name
      type = file.mimetype;
    var uploadpath = __dirname + '/' + name;
    file.mv(uploadpath,function(err){
      if(err){
        console.log("File Upload Failed",name,err);
        res.send("Error Occured! while uploading file")
      }
      else {
        res.send('Request Received. We will send you an email soon');
      }
      console.log("File Uploaded",name);
      email = req.body.emailaddress
      //console.log(email)
      model = req.body.radio
      console.log(model)
      let {PythonShell} = require('python-shell')
      if (model === 'Classification')
        pyshell = new PythonShell('classification.py');
      else
        pyshell = new PythonShell('regression.py');
      pyshell.send(filename);
      pyshell.send(email);
      pyshell.on('message', function (message) {
       console.log(message);  
      }); 
    });
  }
  else {
    res.send("No File selected !");
    res.end();
  };
})


const PORT = process.env.PORT || 4001
app.listen(PORT, () => console.info(`Server has started on ${PORT}`))