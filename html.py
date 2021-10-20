


<!DOCTYPE html>

<html >
<!--From https://codepen.io/frytyler/pen/EGdtg-->
<head>
  <meta charset="UTF-8">
  
  <title>ML API</title>
    
</head>

<body>
 <div class="login">
	<h1 style="text-align: left; color:#00b5a1;margin-top: 1.7%;margin-bottom: 1.7%"><b>Incident Impact Classification</b></h1>
     <!-- Main Input For Receiving Query to our ML -->
	 	 
	<style>		
			
		h1 {color: red;}
		p {color:BLACK;
		font-size: 15px;}
		
		fieldset {
		background-color:#deffe7 ;
		color: ;
		}
		legend {
		padding: 2px;
		border: 1px solid green;
		}
		label{
		display: inline-block;
		margin-left: 50px;
		float: left;
        color:BLACK;
		background-color:
		}		
		
		textarea {
		  width: calc(100% - 12px);
		  height: 75px; 
		  padding: 0.5px;
		  }
		  .testbox {
		  display: block;
		  justify-content: right;
		  
		  
		  padding: 20px;
		 }
		form {
		  width: 99%;
		  padding: 10px;
		  border-radius: 6px;
		  background: ;
		  box-shadow: 0 0 8px #006622; 
		 }			
		
		  input {
		  width: calc(50% - 10px);
		  padding: 5px;
		  size= 30px
		 }  
		  		 
		 .btn-block
		 {float: center}
		 button {
		  width: 95px;
		  padding: 10px;
		  border: none;		  
		  border-radius: 5px; 
		  background:  #00b5a1;
		  font-size: 16px;
		  align: left;
		  cursor: pointer;
		 
		  }
		  button:hover {
		  background:  OLIVE;
		  }
		  		 		  
		  .footer {
		   position:;
		   left: 0;
		   bottom: 0;
		   width: 100%;
		   height: 75px;
		   background-image: linear-gradient(to right, #deffe7 50%, #66ffcc);
		   color: black;
		   text-align: left;
		  }		  
		  
		
	</style>

    <form action="/predict" method="post" style="text-align:right; margin-top: 1.5%; margin-bottom: 1.5%">
		
		<img src="{{url_for('static',filename='CRM.jpg')}}" style="margin-right: 20%; margin-top:0%" width="900" height="300" />
								   
		<fieldset>
			<legend> 
			</legend>
				
					
			<table style="width:100%">
				<tr>												
					<td>
					<label for="category_ID"><b>CATEGORY ID</b></label>
					<input type="number" name="category_ID" placeholder=" " required="required" /></td>			
				
					<td>
					<label for="ID_status"><b>ID_STATUS</b></label>
					<input type="number" name="ID_status" placeholder=" " required="required" /> </td>
					
					<td>
					<label for="opened_time"><b>OPENED TIME</b></label>
					<input type="number" name="opened_time" placeholder=" " required="required" /> </td>
				</tr>	
				
				<tr>
					<td>
					<label for="updated_at"><b>UPDATED AT</b></label>
					<input type="number" name="updated_at" placeholder=" " required="required" /> </td>
										
					<td>
					<label for="Support_group"><b>SUPPORT GROUP</b></label>
					<input type="number" name="Support_group" placeholder=" " required="required" /> </td>
					
					<td>
					<label for="support_incharge"><b>SUPPORT INCHARGE</b></label>
					<input type="number" name="support_incharge" placeholder=" " required="required" /> </td>
				</tr>
				
				<tr>
					<td>
					<label for="Location"><b>LOCATION</b></label>
					<input type="number" name="location" placeholder=" " required="required" /> </td>
					
					<td>				
					<label for="count_updated"><b>COUNT UPDATED</b></label>
					<input type="number" name="count_updated" placeholder=" " required="required" /> </td>
					
					<td>
					<label for="ID_caller"><b>ID_CALLER</b></label>
					<input type="number" name="ID_caller" placeholder=" " required="required" />  </td>
				</tr>			
				
			</table>
			<div class="btn-block" >	
				<button type="submit" style="margin-left:auto;margin-right:auto;display:block;margin-top:0.5%;margin-bottom:0%"><b><i>PREDICT</b></i></button>
			</div>	
					
		</fieldset>

    </form>
	
	<div id="container" style="white-space:nowrap">

    <div id="image" style="display:inline;">
        <img src="{{url_for('static',filename='eye.jpg')}}" width="200" height="130"/>
		
    </div>
	
	<div id="texts" style="display:inline;"> 
        <h1 style="number-align:center; text-align:center;margin-top:1%;margin-bottom:1%;color:#00b5a1;"><b>{{ prediction_text }}</b></h1>
    </div>
    </div>


 </div>
 
<div class="footer">	
	<p><i><b>Team : Rashmi Kulkarni, Shraddha Mankar, Sucharita Mukherjee, Vaishnavi EM </b></i></p>

	<p><i><b>Mentor: Rajashekhar Madishetti</b></i></p>		
	
</div>

</body>
</html>
