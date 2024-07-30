document.addEventListener("DOMContentLoaded", function () {
  // Event listeners to delete Users
  document.querySelectorAll("#delete-user").forEach((button) => {
    button.addEventListener("click", function () {
      const row = this.closest("tr");
      const id = row.dataset.id;

      if (confirm("Are you sure you want to delete this user?")) {
        fetch(`/users/${id}`, {
          method: "DELETE",
          headers: {
            "Content-Type": "application/json",
          },
        })
          .then((response) => {
            if (response.ok) {
              row.remove();
              alert("User deleted successfully!");
            } else {
              alert("Failed to delete the user.");
            }
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
        fetch(`/messages/${id}`, {
          method: "DELETE",
          headers: {
            "Content-Type": "application/json",
          },
        })
          .then((response) => {
            if (response.ok) {
              row.remove();
              alert("Message deleted successfully!");
            } else {
              alert("Failed to delete the message.");
            }
          })
          .catch((error) => {
            console.error("Error:", error);
            alert("An error occurred while deleting the message.");
          });
      }
    });
  });
});
