const textArea = document.getElementById("message");
const charCount = document.getElementById("char-count");

textArea?.addEventListener("input", () => {
  const currentLength = textArea.value.length;
  const maxLength = textArea.getAttribute("maxlength");
  charCount.textContent = `${currentLength} / ${maxLength}`;
});
