const form = document.getElementById("loginForm");
const messageDiv = document.getElementById("message");
const messageText = document.getElementById("messageText");
const buttonText = document.getElementById("buttonText");
const buttonSpinner = document.getElementById("buttonSpinner");

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;

  // Animación de espera en botón
  buttonText.style.display = "none";
  buttonSpinner.style.display = "inline-block";
  form.querySelector('button[type="submit"]').disabled = true;

  try {
    // Formdata para enviar información de Formularios
    const formData = new FormData();
    formData.append("username", email);
    formData.append("password", password);

    const response = await fetch("/auth/jwt/login", {
      method: "POST",
      body: formData,
    });

    let data = null;
    const contentType = response.headers.get("content-type") || "";
    if (contentType.includes("application/json")) {
      data = await response.json();
    }

    if (response.ok) {
      showMessage(
        "¡Sesión iniciada correctamente! Redirigiendo...",
        "success",
      );
      setTimeout(() => {
        window.location.href = "/admin/";
      }, 1500);
    } else {
      let errorMessage;
      if (data?.detail === "LOGIN_BAD_CREDENTIALS" || data?.detail?.includes("Incorrect")) {
        errorMessage = "Correo o contraseña incorrectos. Por favor, intenta de nuevo.";
      } else {
        errorMessage = data?.detail || "Error al iniciar sesión. Intenta de nuevo.";
      }
      showMessage(errorMessage, "danger");
    }
  } catch (error) {
    showMessage("Error: " + error.message, "danger");
  } finally {
    buttonText.style.display = "inline";
    buttonSpinner.style.display = "none";
    form.querySelector('button[type="submit"]').disabled = false;
  }
});

function showMessage(text, type) {
  messageText.textContent = text;
  messageDiv.className = `alert alert-${type} alert-dismissible fade show`;
  messageDiv.style.display = "block";
}

// Botón para cambiar la visbilidad de la contraseña
const togglePasswordBtn = document.getElementById("togglePassword");
const passwordInput = document.getElementById("password");
const toggleIcon = document.getElementById("toggleIcon");

togglePasswordBtn.addEventListener("click", () => {
  const type = passwordInput.type === "password" ? "text" : "password";
  passwordInput.type = type;
  toggleIcon.className = type === "password" ? "fas fa-eye" : "fas fa-eye-slash";
});

const forgotPasswordLink = document.getElementById("forgotPasswordLink");
if (forgotPasswordLink) {
  const forgotPasswordModalEl = document.getElementById("forgotPasswordModal");
  const forgotPasswordModal = forgotPasswordModalEl
    ? new bootstrap.Modal(forgotPasswordModalEl)
    : null;
  const copyEmailButton = document.getElementById("copyEmailButton");
  const supportEmailText = document.getElementById("supportEmailText");
  const supportEmail = supportEmailText?.textContent?.trim() || "";

  if (copyEmailButton) {
    const originalCopyText = copyEmailButton.textContent;
    copyEmailButton.addEventListener("click", async () => {
      let copied = false;
      if (navigator.clipboard?.writeText && supportEmail) {
        try {
          await navigator.clipboard.writeText(supportEmail);
          copied = true;
        } catch (error) {
          copied = false;
        }
      }

      if (copied) {
        copyEmailButton.textContent = "Copiado";
        setTimeout(() => {
          copyEmailButton.textContent = originalCopyText;
        }, 2000);
      } else {
        showMessage(
          "No se pudo copiar el email. Copialo manualmente.",
          "warning",
        );
      }
    });
  }

  forgotPasswordLink.addEventListener("click", (e) => {
    e.preventDefault();
    if (forgotPasswordModal) {
      forgotPasswordModal.show();
    }
  });
}
