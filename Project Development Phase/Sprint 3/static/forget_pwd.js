function validateform(){
var email=document.forms["forgetpwd"]["email"].value;

if (email==null || email==""){
  alert("Email can't be empty");
  return false;
}


else if(!(/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(email))){

  alert("You have entered an invalid email address!");
  return false
}
}