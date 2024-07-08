document.addEventListener("DOMContentLoaded", function () {
  const navbar = document.querySelector(".navbar");

  window.addEventListener("scroll", function () {
    if (window.scrollY > 0) {
      navbar.classList.add("bg-dark");
    } else {
      navbar.classList.remove("bg-dark");
    }
  });
});
