document.addEventListener("DOMContentLoaded", function () {
  let logoEnterActive = false;
  let logoLeaveActive = false;
  const logoActiveMaxWidth = 768;
  const name = "Travel Tales";

  const mouseEnterOnLogo = () => {
    if (window.innerWidth < logoActiveMaxWidth) return;
    if (logoEnterActive || logoLeaveActive) return;

    logoEnterActive = true;
    logo.textContent = "T";

    let index = 1;
    function typeEffect() {
      if (index < name.length) {
        logo.textContent += name[index];
        index++;
        requestAnimationFrame(typeEffect);
      } else {
        logoEnterActive = false;
      }
    }

    typeEffect();
  };

  const mouseLeaveOnLogo = () => {
    if (window.innerWidth < logoActiveMaxWidth) return;
    if (logoLeaveActive) return;
    if (logoEnterActive) {
      setTimeout(mouseLeaveOnLogo, 1000);
      return;
    }

    logoLeaveActive = true;

    let index = logo.textContent.length;

    function typeEffect() {
      if (index > 2) {
        logo.textContent = logo.textContent.slice(0, -1);
        index--;
        requestAnimationFrame(typeEffect);
      } else {
        logo.textContent = "TT";
        logoLeaveActive = false;
      }
    }

    typeEffect();
  };

  const flashMessages = document.querySelectorAll(".alert button.close");
  const logo = document.querySelector(".navbar .logo");
  const menu = document.querySelector("#menu-button");
  const textArea = document.getElementById("message");
  const charCount = document.getElementById("char-count");
  const registerButton = document.getElementById("register-btn");

  const usernameField = document.getElementById("username");
  const passwordField = document.getElementById("password");
  const confirmPasswordField = document.getElementById("confirm-password");

  logo?.addEventListener("mouseleave", mouseLeaveOnLogo);
  logo?.addEventListener("mouseenter", mouseEnterOnLogo);

  menu?.addEventListener("click", () => {
    menu.parentElement.classList.toggle("open");
  });

  flashMessages.forEach((button) => {
    const timeout = setTimeout(() => {
      button.parentElement.remove();
    }, 6000);

    button?.addEventListener("click", function () {
      button.parentElement.remove();
      clearTimeout(timeout);
    });
  });

  textArea?.addEventListener("input", () => {
    const currentLength = textArea.value.length;
    const maxLength = textArea.getAttribute("maxlength");
    charCount.textContent = charCount ? `${currentLength} / ${maxLength}` : "";
  });

  registerButton?.addEventListener("click", (event) => {
    let isValid = true;
    if (/\s/.test(usernameField.value)) {
      usernameField.setCustomValidity(
        "Spaces are not allowed in the username."
      );
      usernameField.reportValidity();
      isValid = false;
    }
    if (passwordField.value !== confirmPasswordField.value) {
      passwordField.setCustomValidity("Passwords must match.");
      confirmPasswordField.setCustomValidity("Passwords must match.");
      passwordField.reportValidity();
      confirmPasswordField.reportValidity();
      isValid = false;
    }

    if (!isValid) {
      event.preventDefault();
    } else {
      usernameField.setCustomValidity("");
      passwordField.setCustomValidity("");
      confirmPasswordField.setCustomValidity("");
    }
  });
});
