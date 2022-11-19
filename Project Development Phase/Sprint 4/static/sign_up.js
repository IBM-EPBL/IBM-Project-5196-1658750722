function validateform(){
var name=document.forms["signup"]["username"].value;
var email=document.forms["signup"]["email"].value;
var password=document.forms["signup"]["password"].value;
var confirmpwd=document.forms["signup"]["confirmpassword"].value;
var country=document.forms["signup"]["country"].value;
var phone=document.forms["signup"]["phone"].value;




if (name==null || name==""){
  alert("Name can't be empty");
  return false;
}

else if (email==null || email==""){
  alert("Email can't be empty");
  return false;
}

else if (password==null || password==""){
  alert("Pasword can't be empty");
  return false;
}

else if (confirmpwd==null || confirmpwd==""){
  alert("Confirm Pasword can't be empty");
  return false;
}
else if(!(/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(email))){

  alert("You have entered an invalid email address!");
  return false
}



else if(password.length<6){
  alert("Password must be at least 6 characters long.");
  return false;
  }
 else if(password!=confirmpwd){
 alert("Password mismatch");
 return false
 }

 else if (country=="select a country"){
  alert("Select a country");
  return false;
}
else if (phone==null || phone==""){
  alert("Phone No can't be empty");
  return false;
}

else if ((phone.length)!=10){
  alert("Enter a valid Phone No");
  return false;
}
}