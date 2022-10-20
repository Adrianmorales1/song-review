const login = document.querySelector(".login");
const register = document.querySelector(".register");
const form = document.querySelector("#form");
const switchs = document.querySelector(".switch");

function tab2(){
    form.style.marginLeft = "-100%";
    login.style.background = "none";
    signup.style.background = "background: linear-gradient(45deg,#00d5fc, #046af6);";
}

function tab1(){
    form.style.marginLeft = "0";
    login.style.background = "none";
    register.style.background = "background: linear-gradient(45deg,#00d5fc, #046af6);";
    switchs[current - 1 ].classList.remove("active");
}