// click or drag file
var fileInput = document.querySelector("input[type=file]");
var filenameContainer = document.querySelector("#filename");
var dropzone = document.querySelector("div");

fileInput.addEventListener("change", function () {
  filenameContainer.innerText = fileInput.value.split("\\").pop();
});

fileInput.addEventListener("dragenter", function () {
  dropzone.classList.add("dragover");
});

fileInput.addEventListener("dragleave", function () {
  dropzone.classList.remove("dragover");
});

// password toggler
function toggler(e) {
  if (e.innerHTML == "Show") {
    e.innerHTML = "Hide";
    document.getElementById("secret_key").type = "text";
  } else {
    e.innerHTML = "Show";
    document.getElementById("secret_key").type = "password";
  }
}
// password toggler
function toggler2(e) {
  if (e.innerHTML == "Show") {
    e.innerHTML = "Hide";
    document.getElementById("aws_access_key").type = "text";
  } else {
    e.innerHTML = "Show";
    document.getElementById("aws_access_key").type = "password";
  }
}
// password toggler
function toggler3(e) {
  if (e.innerHTML == "Show") {
    e.innerHTML = "Hide";
    document.getElementById("auth_token").type = "text";
  } else {
    e.innerHTML = "Show";
    document.getElementById("auth_token").type = "password";
  }
}

// disable submit btn until all fields are filled

const submit_btn = document.getElementById("submit");

submit_btn.disabled = true;
let d = document,
  [inputs] = [d.querySelectorAll("input")];
submit_btn.disabled = true;

for (i = 0; i < inputs.length; i++) {
  inputs[i].addEventListener("input", () => {
    let values = [];
    inputs.forEach((v) => values.push(v.value));
    submit_btn.disabled = values.includes("");
  });
}
//form Submission
const alert = document.querySelector(".alert");
const wait_time = document.querySelector("#wait_time");

submit_btn.onclick = () => {
  alert.classList.add("show");
};
