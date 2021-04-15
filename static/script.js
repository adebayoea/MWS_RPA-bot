const tabs = document.querySelectorAll(" .tabs .tab");
const sections = document.querySelectorAll(" .tab-content");

tabs.forEach((tab) => {
  tab.addEventListener("click", (e) => {
    e.preventDefault();
    removeActiveTab();
    addActiveTab(tab);
  });
});

const removeActiveTab = () => {
  tabs.forEach((tab) => {
    tab.classList.remove("is-active");
  });
  sections.forEach((section) => {
    section.classList.remove("is-active");
  });
};

const addActiveTab = (tab) => {
  tab.classList.add("is-active");
  const href = tab.querySelector("a").getAttribute("href");
  const matchingSection = document.querySelector(href);
  matchingSection.classList.add("is-active");
};

// password toggler
function toggler1(e) {
  if (e.innerHTML == "Show") {
    e.innerHTML = "Hide";
    document.getElementById("password1").type = "text";
  } else {
    e.innerHTML = "Show";
    document.getElementById("password1").type = "password";
  }
}
// password toggler
function toggler2(e) {
  if (e.innerHTML == "Show") {
    e.innerHTML = "Hide";
    document.getElementById("password2").type = "text";
  } else {
    e.innerHTML = "Show";
    document.getElementById("password2").type = "password";
  }
}
// password toggler
function toggler3(e) {
  if (e.innerHTML == "Show") {
    e.innerHTML = "Hide";
    document.getElementById("password3").type = "text";
  } else {
    e.innerHTML = "Show";
    document.getElementById("password3").type = "password";
  }
}

