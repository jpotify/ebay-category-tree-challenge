body = '''
<!doctype html>

<html lang="en">
	<head>
  		<meta charset="utf-8">

		<title>{0}</title>
		<meta name="description" content="{1}">
		<meta name="author" content="Juan Pablo Osorio">
		<meta http-equiv="X-UA-Compatible" content="IE=edge">
		<meta name="viewport" content="width=device-width, initial-scale=1">

		<link rel="stylesheet" href="assets/bootstrap/css/bootstrap.min.css">
		<link rel="stylesheet" href="assets/jstree/dist/themes/default/style.min.css">
		<link rel="stylesheet" href="assets/custom/styles.css">

		<!--[if lt IE 9]>
		<script src="http://html5shiv.googlecode.com/svn/trunk/html5.js"></script>
		<![endif]-->
	</head>

	<body>
		<nav class="navbar navbar-inverse navbar-fixed-top">
		  	<div class="container">
			    <div class="navbar-header">
			    	<button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar" aria-expanded="false" aria-controls="navbar">
				        <span class="sr-only">Toggle navigation</span>
				        <span class="icon-bar"></span>
			      	</button>
			      	<a class="navbar-brand" href="#">Polymath Engineering Challenge</a>
			    </div>
			    <div id="navbar" class="collapse navbar-collapse">
			      	<ul class="nav navbar-nav">
				        <li class="active"><a href="#">{0}</a></li>
			      	</ul>
		    	</div><!--/.nav-collapse -->
		  	</div>
		</nav>

		<div class="container">
			<div class="row">
				<div id="jstree-category"></div>

				<hr />

				<div class="progress">
				  <div class="progress-bar progress-bar-success" role="progressbar" aria-valuenow="100" aria-valuemin="0" aria-valuemax="100" style="width: 100%">
				    100%
				  </div>
				</div>
			</div>
		</div>

		<script src="assets/jquery/dist/jquery-3.0.0.min.js"></script>
  		<script src="assets/jstree/dist/jstree.min.js"></script>

  		<script>
			jQuery(document).ready(function ($) {{
				$('#jstree-category').jstree({{
					'plugins': ["wholerow", "types"],
					'types': {{
						"default": {{ 
							icon: "glyphicon glyphicon-flash" 
						}}
					}},
					'core': {{
						'data': {2}
					}}
				}}).bind("loaded.jstree", function(event, data) {{
					$(this).jstree("open_all");
				}});	
			}});
  		</script>
	</body>
</html>
'''