function validateform(){
var name=document.forms["profile"]["name"].value;
var email=document.forms["profile"]["email"].value;
var password=document.forms["profile"]["password"].value;
var country=document.forms["profile"]["country"].value;
var phone=document.forms["profile"]["phone"].value;




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


else if(!(/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(email))){

  alert("You have entered an invalid email address!");
  return false
}



else if(password.length<6){
  alert("Password must be at least 6 characters long.");
  return false;
  }


if (country==null || country==""){
  alert("Country field is empty");
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

confirm("Are you sure you want to save changes")

}