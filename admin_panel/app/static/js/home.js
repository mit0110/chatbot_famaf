// Cargar información del usuario al iniciar la página
window.addEventListener("load", async () => {
  try {
    const response = await fetch("/auth/users/me");

    if (!response.ok) {
      // Si no está autenticado, redirigir al login
      window.location.href = "/login";
      return;
    }

    const user = await response.json();

    // Poblar los datos del usuario
    document.getElementById("userEmail").textContent = user.email;
    document.getElementById("userFullName").textContent =
      user.full_name || "No especificado";
  } catch (error) {
    console.error("Error al cargar datos del usuario:", error);
    // En caso de error, redirigir al login
    window.location.href = "/login";
  }
});

// Función para cerrar sesión
async function logout() {
  try {
    const response = await fetch("/auth/jwt/logout", {
      method: "POST",
    });

    if (response.ok) {
      window.location.href = "/login";
    } else {
      alert("Error al cerrar sesión. Intenta de nuevo.");
    }
  } catch (error) {
    console.error("Error:", error);
    alert("Error al cerrar sesión.");
  }
}
