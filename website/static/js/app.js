const textArea = document.getElementById("message");
const charCount = document.getElementById("char-count");
const usernameField = document.getElementById("username");
const usernameFieldError = document.querySelector("#username + .field-msg");
const passwordField = document.getElementById("password");
const passwordFieldError = document.querySelector("#password + .field-msg");
const confirmPasswordField = document.getElementById("confirm-password");
const confirmPpasswordFieldError = document.querySelector("#confirm-password + .field-msg");

textArea?.addEventListener("input", () => {
  const currentLength = textArea.value.length;
  const maxLength = textArea.getAttribute("maxlength");
  charCount.textContent = `${currentLength} / ${maxLength}`;
});

document.getElementById("register-btn")?.addEventListener("click", (event) => {
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
})