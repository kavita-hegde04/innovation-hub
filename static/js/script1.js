const form = document.querySelector("div div div div div div div form");

//select email element
eField = document.querySelector(".email");
eInput = eField.querySelector("input");

//select password
pField = document.querySelector(".password");
pInput = pField.querySelector("input");

form.onkeyup = (e) => {
  e.preventDefault(); //preventing from form submitting
  //if email and password is blank then add shake class in it else call specified function
  eInput.value == "" ? eField.classList.add("shake", "error") : checkEmail();
  pInput.value == "" ? pField.classList.add("shake", "error") : checkPass();

  setTimeout(() => {
    //remove shake class after 500ms
    eField.classList.remove("shake");
    pField.classList.remove("shake");

    //add for all fields
  }, 500);

  eInput.onkeyup = () => {
    checkEmail();
  }; //calling checkEmail function on email input keyup
  pInput.onkeyup = () => {
    checkPass();
  }; //calling checkPassword function on pass input keyup

  function checkEmail() {
    //checkEmail function
    let pattern = /^[^ ]+@[^ ]+\.[a-z]{2,3}$/; //pattern for validate email
    if (!eInput.value.match(pattern)) {
      //if pattern not matched then add error and remove valid class
      eField.classList.add("error");
      eField.classList.remove("valid");
      let errorTxt = eField.querySelector(".error-txt");
      //if email value is not empty then show please enter valid email else show Email can't be blank
      eInput.value != ""
        ? (errorTxt.innerText = "Enter a valid email address")
        : (errorTxt.innerText = "Email can't be blank");
    } else {
      //if pattern matched then remove error and add valid class
      eField.classList.remove("error");
      eField.classList.add("valid");
    }
  }

  function checkPass() {
    var numbers = /[0-9]/g;
    var regex = /\W|_/g;
    var upperCaseLetters = /[A-Z]/g;
    //checkPass function
    if (pInput.value == "") {
      //if pass is empty then add error and remove valid class
      pField.classList.add("error");
      pField.classList.remove("valid");
    } else if (pInput.value.length < 8) {
      pField.classList.add("error");
      pField.classList.remove("valid");
    } else if (!pInput.value.match(numbers)) {
      pField.classList.add("error");
      pField.classList.remove("valid");
    } else if (!pInput.value.match(regex)) {
      pField.classList.add("error");
      pField.classList.remove("valid");
    } else if (!pInput.value.match(upperCaseLetters)) {
      pField.classList.add("error");
      pField.classList.remove("valid");
    } else {
      //if pass is empty then remove error and add valid class
      //   pFieldget.innerHTML = "Strong password";
      txt = pField.querySelector(".error-txt");
      pField.classList.remove("error");
      pField.classList.add("valid");
      txt.innerHTML = "Strong password";
    }
  }
};
