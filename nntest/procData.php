<?php
	function RemoveBadVals($str){
		$removeArray = array();
		$strArray = explode(' ', $str);
		foreach($strArray as $key=>$value){
			if((strlen($strArray[$key]) <= 1 && $strArray[$key] !="i")){
				array_push($removeArray,$key);
				$strArray[$key] = "";
			}
			else if($strArray[$key][0] == 'n' && !in_array($strArray[$key][1],array('a','e','i','o','u'))){
				$strArray[$key][0] = "";
				echo $strArray[$key]."<br>";
			}
			else{
				echo $strArray[$key]."<br>";
			}
			trim($strArray[$key], " ");
		}
		
		foreach($removeArray as $key=>$value){
			unset($strArray[$value]);
		}
		
		
		$finalStr = implode(' ', $strArray);
		return $finalStr;
		//$finalEx = explode(' ', $finalStr);
		
		//return implode(' ', $finalEx);
	}




	$myfile = fopen("data/aHR0cHM6Ly8yMDE1YmFzZWJhbGxoYWNrZGF5LmRldnBvc3QuY29t.json", "r") or die("Unable to open file!");
	$data  = fread($myfile,filesize("data/aHR0cHM6Ly8yMDE1YmFzZWJhbGxoYWNrZGF5LmRldnBvc3QuY29t.json"));
	fclose($myfile);
	$jParse = preg_replace('/[^a-z0-9]+/i', ' ',strip_tags($data));
	$jParse = strtolower(strip_tags($jParse));
	//echo $jParse;
	//$jParseArray = RemoveBadVals($jParse);
	$jParseStr = RemoveBadVals($jParse);
	$fp = fopen("test.out","w");
	fwrite($fp,$jParseStr);
	fclose($fp);
	//print_r($jParseArray);
	//json_decode(
	/*
	foreach($jParse as $key=>$value){
		print_r($value);
		echo "<br><br>";
	}*/
	
?>