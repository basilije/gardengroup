<?php
	echo ' <!DOCTYPE html><html><title>The Real Signals Of Your Garden</title><html lang="en">
	<head>  <meta charset="utf-8">  <title>The Real Signals Of Your Garden</title>  <meta name="description" content="The Real Signals Of Your Garden">  <meta name="author" content="Vasilije Mehandzic"></head>
	<style>html, body {    height: 100%;}html {    display: table;    margin: auto;}  body {  background-color:#CDC;  display: table-cell;    vertical-align: top;}  h4{	color:black;  height:42px;  border: none;  box-shadow: -2px 5px 0px -2px grey, 2px 5px 0px -2px grey;}</style>	
	<body><i>__________  something {special}   ! ...</i> <h1 style="color:green;"> GardenGroup </h1><h4>         The Real Signals Of Your Garden     </h4>';
	
	global $to_read,$to_refresh,$last_values_to_plot;   
	$current_folder = "/home/pi/gardengroup/"; 	
	$config_file_name = $current_folder."cfg.cfg";
	$content0 = file_get_contents($config_file_name);
	$ini_array = parse_ini_file($config_file_name);
	$refresh_rate = $ini_array[refresh]*1000;
	$button_style = $ini_array[button_style];
	$default_input = $ini_array[input];
	$to_read = $default_input;
	$default_no_of_values = $ini_array[values];
	require_once("phpChart_Lite/conf.php");
			
	if(isset($_POST['html'])) {
		$content0 = $_POST['html'];
		$myfile0= fopen($config_file_name, "w") or die("Unable to open file0!");
		fwrite($myfile0, $content0);
		fclose($myfile0);			}	
		
	if(isset($_POST['B1'])) { 
		$filename1 = $current_folder.$ini_array['port1'].'.txt';
		$content1 = $_POST['duration1'];
		$myfile1 = fopen($filename1, "w") or die("Unable to open file1!");
		fwrite($myfile1, $content1);
		fclose($myfile1);
		unset($_POST['B1']);	} 
		
	if(isset($_POST['B2'])) { 
		$filename2 = $current_folder.$ini_array['port2'].'.txt';
		$content2 = $_POST['duration2'];
		$myfile2 = fopen($filename2, "w") or die("Unable to open file2!");
		fwrite($myfile2, $content2);
		fclose($myfile2);
		unset($_POST['B2']);	} 
	
	if(isset($_POST['B3'])) { 
		$to_read = $_POST['analog_inputs']; 
		try {$last_values_to_plot = $_POST['duration3'];	}catch (exception $e){  }	
		try{
			if (isset($_POST['to_refresh'])){
				$to_refresh = $_POST['to_refresh'];}
			} catch (exception $e) {}
		unset($_POST['B3']);		}
	
	if(isset($_POST['E1']))
		$content0 = $_POST['html'];
		
	if(isset($_POST['ESC']))
		$to_refresh='off';	
		
	if ($to_refresh=='on')
		echo '<script type="text/javascript">  setInterval("my_function();",'.$refresh_rate.'); function my_function(){ parent.window.location.reload(); }</script>';	

	try {
		$Y = array();	
		if ($last_values_to_plot == '') {	$last_values_to_plot = $default_no_of_values;}
		$ui = (int)$last_values_to_plot*4;	
		$filename = "/home/pi/gardengroup/dbs/".date("Y-m-d").".db";
		$db  = new SQLite3($filename);
		$db->busyTimeout(5000);
		//~ $db->exec('PRAGMA journal_mode = wal;');
		//~ probably there is the smarter way			
		$query_string = "SELECT ".$to_read.",dt FROM records ORDER BY dt DESC";
		$query= $db->query($query_string);
		//~ echo str($query);
		$co = 0;
		while($result=$query->fetchArray()) {
			foreach($result as $ele){
				if ($co<$ui){
					if ($co%4==0){
						$Y[] = $ele;}}
				$co = $co+1;}} 	
		$db->close();					
		unset($db);
	} catch (exception $e) {}		
	
	try {
		$Y = array_reverse($Y);
		$pc4 = new C_PhpChartX(array($Y));
		$pc4->set_title(array('text'=>$to_read.' analog input'));
		$pc4->add_plugins(array('cursor'));    
		$pc4->set_cursor(array('show'=>true,'zoom'=>true));
		$pc4->set_point_labels(array('show'=>false));
		$pc4->set_highlighter(array('show'=>false));
		$pc4->set_axes(array('xaxis'=> array('label'=> 'Last '.$last_values_to_plot.' Values'),'yaxis'=> array('label'=>'Value')));
		$pc4->set_animate(true);
		//~ $pc4->draw(1920/2, 1080/2);
		$pc4->draw();
	} catch (exception $e) {}	
	
	echo '<form method="post">analog-input><select name="analog_inputs" '.$button_style.''.$button_style.'><option value="P0">P0</option><option value="P1">P1</option><option value="P2">P2</option><option value="P3">P3</option><option value="P4">P4</option> <option value="P5">P5</option><option value="P6">P6</option><option value="P7">P7</option>	</select>';
	echo '   last><input type = "Text" '.$button_style.' name = "duration3"> values <input type="checkbox" '.$button_style.'id="to_refresh" name="to_refresh" value="on" ';
	if ($to_refresh=='on'){}else {echo 'un';} echo 'checked>(auto-refresh) <input type="submit" '.$button_style.' name="B3" value="sub-mit"> {!} <input type = "submit" '.$button_style.' name="ESC" value="stop-refresh"/> </form>';
	echo ' <h4 align="right">         The plot     </h4>';

	echo '<h4 align="center">         click on the button to feed the plant    </h4>	<br></br>	
		<form method="post">		<input type = "submit" '.$button_style.' name="B1" value="Turn ON Switch 1 for"/> 		<input type = "Text" '.$button_style.'value ="" name = "duration1"> seconds	</form>  	<br></br>  
		<form method="post"> 		<input type = "submit" '.$button_style.' name="B2" value="Turn ON Switch 2 for"/> 		<input type = "Text" '.$button_style.' value ="" name = "duration2"> seconds	</form>  <br></br>';		
	echo '<h4>       configuration  settings    </h4>  <form action="" method="post"> <textarea name="html"style="width:660px;height:330px;">' . htmlspecialchars($content0) . '</textarea> <input type="submit" '.$button_style.' id="E1" name="E1" value="Save configuration" />';	
			
	echo '<br></br><i>... !you know why?  __________ </i></body></html>';	
?>
