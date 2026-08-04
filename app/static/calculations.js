const token = localStorage.getItem("access_token");

const form = document.getElementById("calculation-form");
const calculationIdInput =
    document.getElementById("calculation-id");
const numberAInput =
    document.getElementById("number-a");
const numberBInput =
    document.getElementById("number-b");
const typeInput =
    document.getElementById("calculation-type");
const submitButton =
    document.getElementById("submit-button");
const cancelButton =
    document.getElementById("cancel-button");
const logoutButton =
    document.getElementById("logout-button");
const calculationList =
    document.getElementById("calculation-list");
const messageBox =
    document.getElementById("message");


if (!token) {
    window.location.href = "/login-page";
}


function getHeaders() {
    return {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`,
    };
}


function showMessage(message, isError = false) {
    messageBox.textContent = message;
    messageBox.className = isError
        ? "message error"
        : "message success";
}


function clearMessage() {
    messageBox.textContent = "";
    messageBox.className = "message";
}


function resetForm() {
    form.reset();
    calculationIdInput.value = "";
    submitButton.textContent = "Add Calculation";
    cancelButton.hidden = true;
}


async function loadCalculations() {
    clearMessage();

    try {
        const response = await fetch(
            "/calculations",
            {
                method: "GET",
                headers: getHeaders(),
            }
        );

        if (response.status === 401) {
            localStorage.removeItem("access_token");
            window.location.href = "/login-page";
            return;
        }

        if (!response.ok) {
            throw new Error(
                "Unable to load calculations."
            );
        }

        const calculations = await response.json();

        displayCalculations(calculations);

    } catch (error) {
        showMessage(error.message, true);
    }
}


function displayCalculations(calculations) {
    if (calculations.length === 0) {
        calculationList.innerHTML =
            "<p>No calculations found.</p>";
        return;
    }

    calculationList.innerHTML = "";

    calculations.forEach((calculation) => {
        const item = document.createElement("div");
        item.className = "calculation-item";

        item.innerHTML = `
            <div>
                <strong>
                    ${calculation.type}
                </strong>
                <p>
                    ${calculation.a} and
                    ${calculation.b}
                    = ${calculation.result}
                </p>
            </div>

            <div class="button-group">
                <button
                    type="button"
                    class="view-button"
                >
                    View
                </button>

                <button
                    type="button"
                    class="edit-button"
                >
                    Edit
                </button>

                <button
                    type="button"
                    class="delete-button"
                >
                    Delete
                </button>
            </div>
        `;

        item
            .querySelector(".view-button")
            .addEventListener(
                "click",
                () => viewCalculation(calculation.id)
            );

        item
            .querySelector(".edit-button")
            .addEventListener(
                "click",
                () => beginEdit(calculation)
            );

        item
            .querySelector(".delete-button")
            .addEventListener(
                "click",
                () => deleteCalculation(calculation.id)
            );

        calculationList.appendChild(item);
    });
}


async function viewCalculation(calculationId) {
    clearMessage();

    try {
        const response = await fetch(
            `/calculations/${calculationId}`,
            {
                method: "GET",
                headers: getHeaders(),
            }
        );

        if (!response.ok) {
            throw new Error(
                "Unable to view calculation."
            );
        }

        const calculation = await response.json();

        showMessage(
            `Calculation ${calculation.id}: ` +
            `${calculation.a} ${calculation.type} ` +
            `${calculation.b} = ${calculation.result}`
        );

    } catch (error) {
        showMessage(error.message, true);
    }
}


function beginEdit(calculation) {
    calculationIdInput.value = calculation.id;
    numberAInput.value = calculation.a;
    numberBInput.value = calculation.b;
    typeInput.value = calculation.type;

    submitButton.textContent = "Update Calculation";
    cancelButton.hidden = false;

    window.scrollTo({
        top: 0,
        behavior: "smooth",
    });
}


async function deleteCalculation(calculationId) {
    const confirmed = window.confirm(
        "Are you sure you want to delete this calculation?"
    );

    if (!confirmed) {
        return;
    }

    clearMessage();

    try {
        const response = await fetch(
            `/calculations/${calculationId}`,
            {
                method: "DELETE",
                headers: getHeaders(),
            }
        );

        if (!response.ok) {
            throw new Error(
                "Unable to delete calculation."
            );
        }

        showMessage(
            "Calculation deleted successfully."
        );

        await loadCalculations();

    } catch (error) {
        showMessage(error.message, true);
    }
}


form.addEventListener(
    "submit",
    async (event) => {
        event.preventDefault();
        clearMessage();

        const numberA =
            Number(numberAInput.value);
        const numberB =
            Number(numberBInput.value);
        const calculationType =
            typeInput.value;
        const calculationId =
            calculationIdInput.value;

        if (
            Number.isNaN(numberA) ||
            Number.isNaN(numberB)
        ) {
            showMessage(
                "Both values must be numbers.",
                true
            );
            return;
        }

        if (
            calculationType === "Divide" &&
            numberB === 0
        ) {
            showMessage(
                "Cannot divide by zero.",
                true
            );
            return;
        }

        const method = calculationId
            ? "PUT"
            : "POST";

        const url = calculationId
            ? `/calculations/${calculationId}`
            : "/calculations";

        try {
            const response = await fetch(
                url,
                {
                    method,
                    headers: getHeaders(),
                    body: JSON.stringify({
                        a: numberA,
                        b: numberB,
                        type: calculationType,
                    }),
                }
            );

            const data = response.status === 204
                ? null
                : await response.json();

            if (!response.ok) {
                const detail = data?.detail;

                throw new Error(
                    typeof detail === "string"
                        ? detail
                        : "Unable to save calculation."
                );
            }

            showMessage(
                calculationId
                    ? "Calculation updated successfully."
                    : "Calculation added successfully."
            );

            resetForm();
            await loadCalculations();

        } catch (error) {
            showMessage(error.message, true);
        }
    }
);


cancelButton.addEventListener(
    "click",
    () => {
        resetForm();
        clearMessage();
    }
);


logoutButton.addEventListener(
    "click",
    () => {
        localStorage.removeItem("access_token");
        window.location.href = "/login-page";
    }
);


loadCalculations();