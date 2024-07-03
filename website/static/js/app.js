document.addEventListener("DOMContentLoaded", function () {
  let logoEnterActive = false;
  let logoLeaveActive = false;
  const logoTime = 60;
  const name = "Travel Tales";

  const mouseEnterOnLogo = () => {
    if (logoEnterActive || logoLeaveActive) return;

    logoEnterActive = true;
    logo.textContent = "T";
  
    function typeEffect(index) {
      if (index < name.length) {
        logo.textContent += name[index];
        setTimeout(() => {
          typeEffect(index + 1);
        }, logoTime);
      } else {
        logoEnterActive = false;
      }
    }
    typeEffect(1);
  };
  
  const mouseLeaveOnLogo = () => {
    if (logoLeaveActive) return;
    if (logoEnterActive) {
      setTimeout(mouseLeaveOnLogo, 1000);
    } else {
      logoLeaveActive = true;
      function typeEffect(index) {
        if (index > 2) {
          logo.textContent = logo.textContent.slice(0, -1);
          setTimeout(() => {
            typeEffect(index - 1);
          }, logoTime);
        } else {
          logo.textContent = "TT";
          logoLeaveActive = false;
        }
      }
      typeEffect(logo.textContent.length);
    }
  };

  const flashMessages = document.querySelectorAll('.alert button.close');
  const logo = document.querySelector('.navbar .logo');
  const textArea = document.getElementById("message");
  const charCount = document.getElementById("char-count");
  const registerButton = document.getElementById("register-btn");

  const usernameField = document.getElementById("username");
  const passwordField = document.getElementById("password");
  const confirmPasswordField = document.getElementById("confirm-password");
  
  logo?.addEventListener('mouseleave', mouseLeaveOnLogo);
  logo?.addEventListener('mouseenter', mouseEnterOnLogo);

  flashMessages?.forEach((button) => {
    button.addEventListener('click', function () {
      const flashMessage = button.parentElement;
      flashMessage.style.display = 'none';
    });
  });

  textArea?.addEventListener("input", () => {
    const currentLength = textArea.value.length;
    const maxLength = textArea.getAttribute("maxlength");
    charCount.textContent = charCount ? `${currentLength} / ${maxLength}` : '';
  });

  registerButton?.addEventListener("click", (event) => {
    let isValid = true;
    if (/\s/.test(usernameField.value)) {
      usernameField.setCustomValidity("Spaces are not allowed in the username.");
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