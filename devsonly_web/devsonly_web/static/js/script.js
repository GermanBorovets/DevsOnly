'use strict';

let key;

const body = document.querySelector('body'),
    sidebar = body.querySelector('nav'),
    toggle = body.querySelector(".toggle"),
    searchBtn = body.querySelector(".search-box"),
    modeSwitch = body.querySelector(".toggle-switch"),
    modeText = body.querySelector(".mode-text"),
    // регистрация
    registrationBox = body.querySelector(".wellcum_block"),
    regInputs = body.querySelectorAll(".wellcum_imp"),
    // посты
    postsInputs = body.querySelectorAll(".add_comment_input"),
    posts = body.querySelectorAll(".post"),
    userTags = body.querySelectorAll(".users_tag"),
    sorter = body.querySelector(".drop_down_menu"),
    sortSub = body.querySelector(".sub-menu"),
    mainItem = body.querySelector(".main-item"),
    sorterLi = body.querySelectorAll(".sort-li");


toggle.addEventListener("click", () => {
    sidebar.classList.toggle("close");
})

modeSwitch.addEventListener("click", () => {
    body.classList.toggle("dark");

    // регистрация
    try {
        registrationBox.classList.toggle("light_box");
    } catch (e) {
        console.log(e);
    }

    // поля
    try {
        get_light_mode(regInputs, "box");
    } catch (e) {
        console.log(e);
    }

    // посты
    try {
        sorter.classList.toggle("light_box");
        sortSub.classList.toggle("light_box");
        mainItem.classList.toggle("light_inp");
        get_light_mode(sorterLi, "text");
        get_light_mode(posts, "box");
        get_light_mode(postsInputs, "text");
        get_light_mode(userTags, "text");
    } catch (e) {
        console.log(e);
    }

    if (body.classList.contains("dark")) {
        modeText.innerText = "Light mode";
    } else {
        modeText.innerText = "Dark mode";

    }
});

function get_light_mode(arr, type){
    for (let index = 0, len = arr.length; index < len; ++index) {
        if (type == "box"){
            arr[index].classList.toggle("light_box"); 
        }else if(type == "text"){
            arr[index].classList.toggle("light_inp"); 
        }
    }
}