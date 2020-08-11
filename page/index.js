const express = require('express');
const cors = require('cors');
const http = require('http');
const hostname = '127.0.0.1';
const port =  8000;

const app = express()
const payload = `
<!doctype html>
<html lang="en">

  <head>
	<title>Accrued payroll tool</title>
    <!-- Required meta tags -->
	<meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- Bootstrap CSS -->
      
		<script src="https://ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js"></script>

		<script src="https://cdnjs.cloudflare.com/ajax/libs/bootstrap-datetimepicker/4.17.47/js/bootstrap-datetimepicker.min.js"
		
		<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js" integrity="sha384-wfSDF2E50Y2D1uUdj0O3uMBJnjuUD4Ih7YwaYd1iqfktj0Uod8GCExl3Og8ifwB6" crossorigin="anonymous"></script>	

		<script src="http://cdn.rawgit.com/Eonasdan/bootstrap-datetimepicker/a549aa8780dbda16f6cff545aeabc3d71073911e/src/js/bootstrap-datetimepicker.js"></script>
	
		<link href="http://cdn.rawgit.com/Eonasdan/bootstrap-datetimepicker/a549aa8780dbda16f6cff545aeabc3d71073911e/build/css/bootstrap-datetimepicker.css" rel="stylesheet"/>

		<link href="https://stackpath.bootstrapcdn.com/bootswatch/4.4.1/cerulean/bootstrap.min.css" rel="stylesheet" integrity="sha384-LV/SIoc08vbV9CCeAwiz7RJZMI5YntsH8rGov0Y2nysmepqMWVvJqds6y0RaxIXT" crossorigin="anonymous">

		<script type="text/javascript" src="/scripts/jquery.min.js"></script>
 		<script type="text/javascript" src="/scripts/moment.min.js"></script>
  		<script type="text/javascript" src="/scripts/bootstrap.min.js"></script>
  		<script type="text/javascript" src="/scripts/bootstrap-datetimepicker.*js"></script>	


	<style>
    
	.container { /* div wrapping forms only */
		padding: 30px 50px 30px 50px;
        margin: 3% 0 0 3%;
        position: center;
        border: 1px solid #CCC;
    }
   
	.navbar {
        background-color: #830703;
        position: relative;
        min-height: 54px;
    
 	}
  	.navbar-brand{ /*class containing logo */
      
  	}
   
  	.custom-file-input {
        border: 1px solid #808080;
  	}
    
  	.pointer {
        cursor: pointer;
  	}
    
  	input[type="file"] { 
        margin: 10px 0px 10px 0px; 
        opacity: 0; /* make transparent */
        z-index: -1; /* move under anything else */
    }
	
	.custom-file-label { /* label for file input */
        margin: 10px 0px 10px 0px; 
        border: 1px solid #808080;
	}
    
	input[type="date"] { 
        margin: 10px 10px 10px 0px; 
        border: 1px solid #808080;
	}
    
	.submission { /*div containing submit button */
		position: relative;
		border: 0px solid #000;
	}

  	.submission button { 
        background: #830703; 
        color: #fff;
    }

	.submission button:hover { /*div containing submit button */
        border:0px solid #e08c89;
        background: #e08c89;
        color: #000;
	}	


	</style>


  </head>
  <body>
  <div class="navbar"
      <div class="navbar-brand">
          <img src="https://www.potsdamcoop.com/sites/default/files/logo-pc-200_0.png" alt="home" id="logo">
      </div>
  </div>
	<form method=post action="https://us-central1-cryptic-wonder-195618.cloudfunctions.net/pp" enctype=multipart/form-data>
		<div class="container">
          <div class="form-group row">
              <div class="col-sm-6">
                <label for="raw_csv" class="custom-file-label pointer"><p class="text-secondary">Choose file</p></label>
                <input type="file" class="custom-file-input" id="raw_csv" name="raw_csv">
              </div>
              <div class="col-sm-6">
                <input type="date" class="form-control" name="raw_date" id="datetimepicker1">
              </div>
           </div>
         <div class="submission row">
          <button type="submit" class="btn">Submit</button>
        </div>
    </div>
	</form>

   <script type="text/javascript" src="https://cdn.jsdelivr.net/npm/bs-custom-file-input/dist/bs-custom-file-input.js">

      $(document).ready(function () {
        bsCustomFileInput.init()
      })

      </script>

      <script type="application/javascript">
          $('input[type="file"]').change(function(e){
              var fileName = e.target.files[0].name;
              $('.custom-file-label').html(fileName);
          });


       $(function () {
              $('#datetimepicker1').datetimepicker();
            });

    </script>
	
      
    </body>
  </html>
`

// landing page
app.get("/", (req, res) => {
  res.set('Content-Type', 'text/html');
  res.status(200).send(new Buffer.from(payload));
});

// remove express trailing slash requirement from inbound url
// express requires trailing slash on the default endpoint, yuck
const merepage = http.createServer((request, response) => {
  if (!request.path) {
    request.url = `/${request.url}` // prepend '/' to keep query params if any
  }
  return app(request, response)
})

module.exports = {
  merepage
}

