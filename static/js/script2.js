const form = document.querySelector("div div div div div div div form");

//select email element
eField = document.querySelector(".email");
eInput = eField.querySelector("input");

//select password
pField = document.querySelector(".password");
pInput = pField.querySelector("input");

//select password2
p2Field = document.querySelector(".password2");
p2Input = p2Field.querySelector("input");

//select fname
fnameField = document.querySelector(".fname");
fnameInput = fnameField.querySelector("input");

//select lname
lnameField = document.querySelector(".lname");
lnameInput = lnameField.querySelector("input");

//select phone
phoneField = document.querySelector(".phone");
phoneInput = phoneField.querySelector("input");

//select department
deptField = document.querySelector(".dept");
deptInput = deptField.querySelector("input");

form.onkeyup = (e) => {
  e.preventDefault(); //preventing from form submitting
  //if email and password is blank then add shake class in it else call specified function
  eInput.value == "" ? eField.classList.add("shake", "error") : checkEmail();
  pInput.value == "" ? pField.classList.add("shake", "error") : checkPass();
  p2Input.value == "" ? p2Field.classList.add("shake", "error") : checkPass2();
  fnameInput.value == ""
    ? fnameField.classList.add("shake", "error")
    : checkFname();

  lnameInput.value == ""
    ? lnameField.classList.add("shake", "error")
    : checkLname();

  phoneInput.value == ""
    ? phoneField.classList.add("shake", "error")
    : checkPhone();

  deptInput.value == ""
    ? deptField.classList.add("shake", "error")
    : checkDept();

  setTimeout(() => {
    //remove shake class after 500ms
    eField.classList.remove("shake");
    pField.classList.remove("shake");
    p2Field.classList.remove("shake");
    fnameField.classList.remove("shake");
    lnameField.classList.remove("shake");
    phoneField.classList.remove("shake");
    deptField.classList.remove("shake");

    //add for all fields
  }, 500);

  eInput.onkeyup = () => {
    checkEmail();
  }; //calling checkEmail function on email input keyup
  pInput.onkeyup = () => {
    checkPass();
  }; //calling checkPassword function on pass input keyup
  p2Input.onkeyup = () => {
    checkPass2();
  }; //calling checkPassword function on pass input keyup
  fnameInput.onkeyup = () => {
    checkFname();
  }; //calling checkPassword function on pass input keyup
  lnameInput.onkeyup = () => {
    checkLname();
  }; //calling checkPassword function on pass input keyup

  phoneInput.onkeyup = () => {
    checkPhone();
  }; //calling checkPassword function on pass input keyup

  deptInput.onkeyup = () => {
    checkDept();
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

  function checkPass2() {
    //checkPass function
    if (p2Input.value == "") {
      //if pass is empty then add error and remove valid class
      pField.classList.add("error");
      pField.classList.remove("valid");
    } else if (pInput.value != p2Input.value) {
      p2Field.classList.add("error");
      p2Field.classList.remove("valid");
    } else {
      //if pass is empty then remove error and add valid class
      p2Field.classList.remove("error");
      p2Field.classList.add("valid");
    }
  }

  function checkFname() {
    var numbers = /[0-9]/g;
    var regex = /\W|_/g;
    if (fnameInput.value == "") {
      fnameField.classList.add("error");
      fnameField.classList.remove("valid");
    } else if (fnameInput.value.match(numbers)) {
      fnameField.classList.add("error");
      fnameField.classList.remove("valid");
    } else if (fnameInput.value.match(regex)) {
      fnameField.classList.add("error");
      fnameField.classList.remove("valid");
    } else if (!fnameInput.value.trim().length) {
      fnameField.classList.add("error");
      fnameField.classList.remove("valid");
    } else {
      fnameField.classList.remove("error");
      fnameField.classList.add("valid");
    }
  }

  function checkLname() {
    var numbers = /[0-9]/g;
    var regex = /\W|_/g;
    if (lnameInput.value == "") {
      lnameField.classList.add("error");
      lnameField.classList.remove("valid");
    } else if (lnameInput.value.match(numbers)) {
      lnameField.classList.add("error");
      lnameField.classList.remove("valid");
    } else if (lnameInput.value.match(regex)) {
      lnameField.classList.add("error");
      lnameField.classList.remove("valid");
    } else if (!lnameInput.value.trim().length) {
      lnameField.classList.add("error");
      lnameField.classList.remove("valid");
    } else {
      lnameField.classList.remove("error");
      lnameField.classList.add("valid");
    }
  }

  function checkPhone() {
    if (phoneInput.value == "") {
      //if pass is empty then add error and remove valid class
      phoneField.classList.add("error");
      phoneField.classList.remove("valid");
    } else if (phoneInput.value.length < 10) {
      phoneField.classList.add("error");
      phoneField.classList.remove("valid");
    } else {
      //if pass is empty then remove error and add valid class
      phoneField.classList.remove("error");
      phoneField.classList.add("valid");
    }
  }

  function checkDept() {
    if (deptInput.value == "") {
      deptField.classList.add("error");
      deptField.classList.remove("valid");
    } else {
      deptField.classList.remove("error");
      deptField.classList.add("valid");
    }
  }
};
