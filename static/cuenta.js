document.addEventListener("DOMContentLoaded", () => {
    const userData = {
        nombre: "Juan",
        apellido: "Pérez",
        mail: "juan.perez@example.com",
        contraseña: "password123",
        direccion: "Calle Falsa 123",
        telefono: "123456789"
    };

    document.getElementById("nombre").value = userData.nombre;
    document.getElementById("apellido").value = userData.apellido;
    document.getElementById("mail").value = userData.mail;
    document.getElementById("contraseña").value = userData.contraseña;
    document.getElementById("direccion").value = userData.direccion;
    document.getElementById("telefono").value = userData.telefono;
});

function updateAccount() {
    const nombre = document.getElementById("nombre").value;
    const apellido = document.getElementById("apellido").value;
    const mail = document.getElementById("mail").value;
    const contraseña = document.getElementById("contraseña").value;
    const direccion = document.getElementById("direccion").value;
    const telefono = document.getElementById("telefono").value;

    alert("Datos actualizados correctamente.");
}