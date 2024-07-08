document.addEventListener("DOMContentLoaded", () => {
    const loginForm = document.getElementById("loginForm");
    const forgotPasswordForm = document.getElementById("forgotPasswordForm");
    const forgotPasswordLink = document.getElementById("forgotPasswordLink");
    const backToLoginLink = document.getElementById("backToLoginLink");
    const recoverPasswordButton = document.getElementById("recoverPasswordButton");
    const confirmationMessage = document.getElementById("confirmationMessage");

    forgotPasswordLink.addEventListener("click", (e) => {
        e.preventDefault();
        loginForm.classList.remove("active-form");
        forgotPasswordForm.classList.add("active-form");
    });

    backToLoginLink.addEventListener("click", (e) => {
        e.preventDefault();
        forgotPasswordForm.classList.remove("active-form");
        loginForm.classList.add("active-form");
    });

    recoverPasswordButton.addEventListener("click", (e) => {
        e.preventDefault();
        confirmationMessage.textContent = "Revisa tu correo para recuperar tu contraseña.";
        confirmationMessage.style.display = "block";
    });
});