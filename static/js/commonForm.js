const fondosCheckbox = document.querySelector("#id_fondos");
const parte2Container = document.querySelector("#parte2_container");
const formFabrica = document.querySelector("#formFabrica");
const requiredFields = parte2Container.querySelectorAll(
    "input, textarea, select"
);

function toggleParte2() {
    if (fondosCheckbox.checked) {
        parte2Container.style.display = "block";
        // Hacer los campos requeridos
        requiredFields.forEach((field) => field.setAttribute("required", ""));
    } else {
        parte2Container.style.display = "none";
        // Eliminar el atributo requerido de los campos ocultos
        requiredFields.forEach((field) => {
            field.removeAttribute("required");
        });
    }
}

toggleParte2();

fondosCheckbox.addEventListener("change", toggleParte2);

// Lógica de limpiar campos solo si existe el botón btnLimpiar
const btnLimpiar = document.querySelector("#btnLimpiar");
if (btnLimpiar) {
    btnLimpiar.addEventListener("click", function () {
        const inputsAll = formFabrica.querySelectorAll(
            'input[type="text"], textarea, input[type="number"]'
        );
        inputsAll.forEach((input) => {
            input.value = "";
            localStorage.removeItem(input.name);
        });

        const placeholderText = document.getElementById("placeholderText");
        if (placeholderText) {
            placeholderText.innerText = "";
        }

        // Limpiar campos de parte2Container si es visible
        if (parte2Container.style.display === "block") {
            requiredFields.forEach((field) => (field.value = ""));
        }
    });
}
