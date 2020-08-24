<!DOCTYPE html>
<html>
<title>gardengroup</title>


<style>
html, body {
    height: 100%;
}

html {
    display: table;
    margin: auto;
}

body {
    display: table-cell;
    vertical-align: top;
}
h4
{
	color:black;
  height:42px;
  border: none;
  box-shadow: -2px 5px 0px -2px grey, 2px 5px 0px -2px grey;
}

</style>	

<head> 
    <title> Garden Group</title> 
</head> 

<body>
	<i>__________  something {special}   ! ...</i>
	<h1 style="color:green;">        Garden Group   </h1>		
	<h4>         click on the button to feed the plant    </h4>

	<br></br>
	<form method="post">
		<input type = "submit" style="height:42px;" name="B1" value="Turn ON Switch 1 for"/> 
		<input type = "Text" style="height:42px;"value ="" name = "duration1"> seconds
	</form>  
	<br></br>  
	<form method="post"> 
		<input type = "submit" style="height:42px;" name="B2" value="Turn ON Switch 2 for"/> 
		<input type = "Text" style="height:42px;" value ="" name = "duration2"> seconds
	</form>        
	<br></br>
	<form method="post"> 
		<select name="analog_inputs" style="height:42px;"><option value="P0">P0</option><option value="P1">P1</option><option value="P2">P2</option><option value="P3">P3</option><option value="P4">P4</option> <option value="P5">P5</option><option value="P6">P6</option><option value="P7">P7</option>
		</select> last <input type = "Text" style="height:42px;" name = "duration3">
		values <input type="submit" style="height:42px;" name="B3">		
		<input type="checkbox" style="height:42px;"id="to_refresh" name="to_refresh" value="on" checked>(auto)
		<input type = "submit" style="height:42px;" name="F5" value="REFRESH"/> 
		<input type = "submit" style="height:42px;" name="ESC" value="ESCAPE"/> 
	</form> 
	<br></br>

    <?php
    global $to_read;
    $to_read = "P0";
    global $to_refresh;
    global $until_element;    



	require_once("phpChart_Lite/conf.php");

	if(isset($_POST['F5'])) { 
		ini_set('display_errors', 'Off');
	}
	if(isset($_POST['ESC'])) { 
		ini_set('display_errors', 'On');
	}



	if(isset($_POST['B1'])) { 
		$filename1 = "/home/pi/gardengroup/20.txt";
		$content1 = $_POST['duration1'];
		$myfile1 = fopen($filename1, "w") or die("Unable to open file1!");
		fwrite($myfile1, $content1);
		fclose($myfile1);
		unset($_POST['B1']);
	} 

	if(isset($_POST['B2'])) { 
		$filename2 = "/home/pi/gardengroup/18.txt";
		$content2 = $_POST['duration2'];
		$myfile2 = fopen($filename2, "w") or die("Unable to open file2!");
		fwrite($myfile2, $content2);
		fclose($myfile2);
		unset($_POST['B2']);
	}          

	if(isset($_POST['B3'])) { 
		$to_read = $_POST['analog_inputs'];  // Storing Selected Value In Variable
		try {$until_element = $_POST['duration3'];	}catch (exception $e){  }
		unset($_POST['B3']);		
		try{
			if (isset($_POST['to_refresh'])){
				$to_refresh = $_POST['to_refresh'];}
			} catch (exception $e) {}
	}

	if(isset($_POST['E1'])) { 
		$content0 = $_POST['html'];  // Storing Selected Value In Variable
	}

	try {

		$Y = array();		
		//~ try {$until_element = $_POST['duration3'];	}catch (exception $e){  }			
		if ($until_element == '') {	$until_element = 42;}
		$ui = (int)$until_element*4;	
		$filename = "/home/pi/gardengroup/dbs/".date("Y-m-d").".db";
		$db_handle  = new SQLite3($filename);
		//~ $query_string = "SELECT * FROM records ORDER BY dt DESC";

		//~ probably there is the smarter way			
		$query_string = "SELECT ".$to_read.",dt FROM records ORDER BY dt DESC";
		try {
			$query= $db_handle->query($query_string);
				try {
						$result=$query->fetchArray();		
						$co = 0;
						try {
							while($result=$query->fetchArray()) {		
								foreach($result as $ele){
									if ($co<$ui){
										if ($co%4==0){
											$Y[] = $ele;
										}
									}
									$co = $co+1;
								}
							} 
						} catch (exception $e) {}	
					} catch (exception $e) {}
				} catch (exception $e) {}
	} catch (exception $e) {}


	if ($to_refresh=='on'){
				echo '<script type="text/javascript">';
				echo '  setInterval("my_function();",5000); ';				 
				echo '    function my_function(){';
				echo '  parent.window.location.reload();';
				echo '    }';
				echo '</script>';
		}			

	$pc4 = new C_PhpChartX(array($Y),'Graph');
	$pc4->set_animate(true);
	$pc4->add_plugins(array('canvasTextRenderer','canvasAxisTickRenderer','highlighter','canvasOverlay','cursor','pointLabels'),true);
	$pc4->set_title(array('text'=>$to_read));    
	$pc4->set_cursor(array('show'=>false));
	$pc4->set_point_labels(array('show'=>false));
	$pc4->set_highlighter(array('show'=>false));
	$pc4->set_axes(array(			'xaxis'=> array('label'=> 'Last '.$until_element.' Values'),
			'yaxis'=> array('label'=>'Value')		));
	$pc4->draw(800,500);

    $config_file_name = "/home/pi/gardengroup/cfg.cfg";
	if(isset($_POST['html'])) {
		$content0 = $_POST['html']; // You want to make this more secure!		
		$myfile0= fopen($config_file_name, "w") or die("Unable to open file0!");
		fwrite($myfile0, $content0);
		fclose($myfile0);		
	}

	echo '<h4>       configuration  settings    </h4> ';
	echo ' <form action="" method="post">';
    $content0 = file_get_contents($config_file_name);
    echo '<textarea name="html"style="width:660px;height:330px;">' . htmlspecialchars($content0) . "</textarea>";
    echo ' <input type="submit" style="height:42px;" id="E1" name="E1" value="Save confgiguration" />';
	echo '<h4>       special  commands    </h4> ';
	$db_handle->close();	
  ?>
      <br></br>
<i>... !you know why?  __________ </i>

</body>
