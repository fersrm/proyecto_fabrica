const fondosCheckbox = document.querySelector("#id_fondos");
const parte2Container = document.querySelector("#parte2_container");
const formFabrica = document.querySelector("#formFabrica");
const textareas = document.querySelectorAll("textarea");
const btnLimpiar = document.querySelector("#btnLimpiar");
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

        // Reiniciar el contador de caracteres de todos los textareas
        textareas.forEach(function (textarea) {
            const updateCounter = () => {
                const currentLength = textarea.value.length;
                const maxLength = textarea.getAttribute("maxlength");
                const counter =
                    textarea.parentNode.querySelector(".char-counter");
                if (counter) {
                    counter.textContent = `${currentLength}/${maxLength}`;
                }
            };
            updateCounter(); // Llama a la función de actualización del contador
        });
    });
}

// Lógica input files
(function (document, window) {
    const inputs = document.querySelectorAll('input[type="file"]');

    inputs.forEach(function (input) {
        const label = input.nextElementSibling;
        const labelVal = label ? label.innerHTML : "";

        input.addEventListener("change", function (e) {
            let fileName = "";
            if (this.files && this.files.length > 1) {
                fileName = `${this.files.length} archivos seleccionados`;
            } else {
                fileName = e.target.value.split("\\").pop();
            }

            if (label) {
                const span = label.querySelector("span");
                if (span) {
                    span.innerHTML = fileName;
                } else {
                    label.innerHTML = fileName || labelVal;
                }
            }
        });
    });
})(document, window);

// lógica de conteo de letras
textareas.forEach(function (textarea) {
    const maxLength = textarea.getAttribute("maxlength");
    const counter = document.createElement("div");
    counter.className = "char-counter";
    counter.style.fontSize = "0.9em";
    counter.style.textAlign = "right";
    counter.style.color = "#666";
    textarea.parentNode.appendChild(counter);

    const updateCounter = () => {
        const currentLength = textarea.value.length;
        counter.textContent = `${currentLength}/${maxLength}`;
    };

    textarea.addEventListener("input", updateCounter);
    updateCounter();
});
