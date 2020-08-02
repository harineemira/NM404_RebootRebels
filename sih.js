const {spawn} = require('child_process');

function showProgressBar() {
    document.getElementById("progressBar").style.display = "block";
  }

function hideProgressBar() {
    document.getElementById("progressBar").style.display = "none";
  }

function showLoader() {
    document.getElementById("loader").style.display = "block";
  }

function hideLoader() {
    document.getElementById("loader").style.display = "none";
  }

function openOutput() {
    var input='xyzcxc'; 
    var dataToSend;
    // spawn new child process to call the python script
    const python = spawn('python', ['disp_mask.py', `${input}`]);
    python.stdout.on('data', function (data) {
    console.log('Pipe data from python script ...');
    dataToSend = data.toString();
    });
    // in close event we are sure that stream from child process is closed
    python.on('close', (code) => {
    console.log(`child process close all stdio with code ${code}`);
    console.log(dataToSend);
    });
  }

function output() {
    window.open("geoJsonMap.html", "Ship Detection", "toolbar=yes,scrollbars=yes,resizable=yes,top=500,left=500,width=400,height=400");
  }

function prevw(){

    var input=document.getElementById("validatedCustomFile").value;  
    var filename = input.replace(/^.*\\/, "");
    f2 = filename.replace("zip", "SAFE");   
    f3 = "\\preview\\quick-look.png";
    f4=f2.concat("\\",f3)     
    console.log(f4);     
    document.getElementById('myImage').src=f4;  
}

function unzippy(){   
    var input=document.getElementById("validatedCustomFile").value;  
    var filename = input.replace(/^.*\\/, ""); 
    console.log(filename);
    var dataToSend;
    // spawn new child process to call the python script
    const python = spawn('python', ['unzip.py', `${filename}`]);
    // collect data from script
    python.stdout.on('data', function (data) {
    console.log('Pipe data from python script ...');
    dataToSend = data.toString();
    });
    // in close event we are sure that stream from child process is closed
    python.on('close', (code) => {
    console.log(`child process close all stdio with code ${code}`);
    console.log(dataToSend);
    hideLoader();
    });
    
} 

function landmask(){   

    var input=document.getElementById("validatedCustomFile").value;  
    var filename = input.replace(/^.*\\/, "");
    console.log(filename);
    var dataToSend;
    // spawn new child process to call the python script
    const python = spawn('python', ['land-mask.py', `${filename}`]);
    // collect data from script
    python.stdout.on('data', function (data) {
    console.log('Pipe data from python script ...');
    dataToSend = data.toString();
    });
    // in close event we are sure that stream from child process is closed
    python.on('close', (code) => {
    console.log(`child process close all stdio with code ${code}`);
    console.log(dataToSend);
    hideProgressBar();
    openOutput();
    });
   
} 

function seamask(){   

    var input=document.getElementById("validatedCustomFile").value;  
    var filename = input.replace(/^.*\\/, "");
    console.log(filename);
    var dataToSend;
    // spawn new child process to call the python script
    const python = spawn('python', ['sea-mask.py', `${filename}`]);
    // collect data from script
    python.stdout.on('data', function (data) {
    console.log('Pipe data from python script ...');
    dataToSend = data.toString();
    });
    // in close event we are sure that stream from child process is closed
    python.on('close', (code) => {
    console.log(`child process close all stdio with code ${code}`);
    console.log(dataToSend);
    hideProgressBar();
    openOutput();
    });   
} 

function shipdetection(){

    var input=document.getElementById("validatedCustomFile").value;  
    var filename = input.replace(/^.*\\/, "");
    console.log(filename);
    var dataToSend;
    // spawn new child process to call the python script
    const python = spawn('python', ['electron-ship.py', `${filename}`]);
    // collect data from script
    python.stdout.on('data', function (data) {
    console.log('Pipe data from python script ...');
    dataToSend = data.toString();
    });
    // in close event we are sure that stream from child process is closed
    python.on('close', (code) => {
    console.log(`child process close all stdio with code ${code}`);
    console.log(dataToSend);
    hideProgressBar();
    output();
    });
    
} 

function openJSON(){   
    var input='xyzcxc'; 
    var dataToSend;
    // spawn new child process to call the python script
    const python = spawn('python', ['openjson.py', `${input}`]);
    python.stdout.on('data', function (data) {
    console.log('Pipe data from python script ...');
    dataToSend = data.toString();
    });
    // in close event we are sure that stream from child process is closed
    python.on('close', (code) => {
    console.log(`child process close all stdio with code ${code}`);
    console.log(dataToSend);
    });
} 

function openCSV(){   
    var input='xyzcxc'; 
    var dataToSend;
    // spawn new child process to call the python script
    const python = spawn('python', ['opencsv.py', `${input}`]);
    python.stdout.on('data', function (data) {
    console.log('Pipe data from python script ...');
    dataToSend = data.toString();
    });
    // in close event we are sure that stream from child process is closed
    python.on('close', (code) => {
    console.log(`child process close all stdio with code ${code}`);
    console.log(dataToSend);
    });
} 
