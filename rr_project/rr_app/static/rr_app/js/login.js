document.getElementById("loginForm").addEventListener("submit", function(e) {
  e.preventDefault();

  let email = document.getElementById("email");
  let password = document.getElementById("password");
  let errorMsg = document.getElementById("errorMsg");

  // Reset styles
  email.classList.remove("error");
  password.classList.remove("error");
  errorMsg.style.display = "none";

  // Simple validation
  if (email.value === "test@example.com" && password.value === "1234") {
    alert("✅ Login successful!");
  } else {
    errorMsg.textContent = "Email or password is incorrect";
    errorMsg.style.display = "block";
    email.classList.add("error");
    password.classList.add("error");
  }
});
