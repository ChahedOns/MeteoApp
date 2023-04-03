# MeteoApp
#API enty points : 
*********************** Authentification ************************

#Register : http://127.0.0.1:5000/register (method = post ) ( entry data -> form with 5 inputs : mail , name ,pwd , birth_date(yyyy-mm-dd) and location ( string) )
#Login : http://127.0.0.1:5000/login (method = post)( entry data -> form : mail + pwd )
#Logout : http://127.0.0.1:5000/logout(method = post)
#Profile : http://127.0.0.1:5000/profile(method = post)

************************* Weather ******************************

#Get current weather of a specific city : http://127.0.0.1:5000/weather (method=POST) ( entry data -> form 1 input : city ( string) ) 
#Get all weather saved data of a specific city : http://127.0.0.1:5000/weather (method=GET) ( entry data -> form 1 input : city ( string) ) 
#To use those APIs you should be logged in :
  #Get history weather of a specific city : http://127.0.0.1:5000/history ( method=GET) entry data -> form 1 input  : city(string)
  #Get forcast weather of a specific city : http://127.0.0.1:5000/forcast ( method=POST) entry data -> form 1input : city (string 

*********************** Notification ********************************



