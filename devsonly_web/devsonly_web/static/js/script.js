'use strict';

let key;
const body = document.querySelector('body'),
    sidebar = body.querySelector('nav'),
    toggle = body.querySelector(".toggle"),
    searchBtn = body.querySelector(".search-box"),
    modeSwitch = body.querySelector(".toggle-switch"),
    modeText = body.querySelector(".mode-text"),
    registrationBox = body.querySelector(".wellcum_block"),
    inputs = body.querySelectorAll('.wellcum_imp');


toggle.addEventListener("click", () => {
    sidebar.classList.toggle("close");
})

modeSwitch.addEventListener("click", () => {
    body.classList.toggle("dark");
    registrationBox.classList.toggle("light_box");
    
    for (key in inputs){
        inputs[key].classList.toggle("light_inp");
    }

    if (body.classList.contains("dark")) {
        modeText.innerText = "Light mode";
    } else {
        modeText.innerText = "Dark mode";

    }
});