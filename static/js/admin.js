document.addEventListener("DOMContentLoaded", function () {
  // Event listeners to delete Users
  document.querySelectorAll("#delete-user").forEach((button) => {
    button.addEventListener("click", function () {
      const row = this.closest("tr");
      const id = row.dataset.id;

      if (confirm("Are you sure you want to delete this user?")) {
        fetch(`/api/users/${id}`, {
          method: "DELETE",
          headers: {
            "Content-Type": "application/json",
          },
        })
          .then((response) => response.json())
          .then((data) => {
            if (data.status === "deleted") {
              row.remove();
            }
            alert(data.message);
          })
          .catch((error) => {
            console.error("Error:", error);
            alert("An error occurred while deleting the user.");
          });
      }
    });
  });

  // Event listeners to delete Messages
  document.querySelectorAll("#delete-message").forEach((button) => {
    button.addEventListener("click", function () {
      const row = this.closest("tr");
      const id = row.dataset.id;

      if (confirm("Are you sure you want to delete this message?")) {
        fetch(`/api/messages/${id}`, {
          method: "DELETE",
          headers: {
            "Content-Type": "application/json",
          },
        })
          .then((response) => response.json())
          .then((data) => {
            if (data.status === "deleted") {
              row.remove();
            }
            alert(data.message);
          })
          .catch((error) => {
            console.error("Error:", error);
            alert("An error occurred while deleting the message.");
          });
      }
    });
  });
});
