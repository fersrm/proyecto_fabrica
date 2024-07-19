const form = document.getElementById("formFabrica");
const inputs = form.querySelectorAll(
    'input[type="text"], textarea, input[type="number"]'
);
const placeholderTextDiv = document.getElementById("placeholderText");

// Cargar valores desde localStorage
inputs.forEach((input) => {
    const storedValue = localStorage.getItem(input.name);
    if (storedValue) {
        input.value = storedValue;
    }

    // Mostrar el placeholder en el contenedor al enfocar
    input.addEventListener("focus", () => {
        placeholderTextDiv.innerText = input.placeholder;
    });

    // Guardar en localStorage al cambiar
    input.addEventListener("input", () => {
        localStorage.setItem(input.name, input.value);
    });
});

// Limpiar localStorage al enviar el formulario
form.addEventListener("submit", () => {
    inputs.forEach((input) => {
        localStorage.removeItem(input.name);
    });
});
