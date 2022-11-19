function validateform(){
var email=document.forms["signin"]["email"].value;
var pass=document.forms["signin"]["password"].value;

if (email==null || email==""){
  alert("Email can't be empty");
  return false;
}

else if (pass==null || pass==""){
  alert("Password can't be empty");
  return false;
}

else if(!(/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(email))){

  alert("You have entered an invalid email address!");
  return false
}
}