const express = require('express');
const app = express();
const port = (process.env.PORT || 3500);
const path = require('path');
const bodyParser = require('body-parser');

const spawn = require("child_process").spawn;

app.use(bodyParser.json());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(bodyParser.urlencoded({ extended: true }));

app.get('/', function(req, res){
  res.sendFile(path.join(__dirname + '/src/index.html'));
});
app.post('/', function(req, res){
  let text = req.body.text;
  const pythonProcess = spawn('python',["/src/py.py", text]);
  pythonProcess.stdout.on('data', (data) => {
    res.send(data);
  });
});

app.listen(port, () => console.log(`app listening on port ${port}!`));