let memberCounter = 1; // Counter for unique 'name' attributes

document.getElementById("addOptionButton").addEventListener("click", function () {
    const dynamicFields = document.getElementById("dynamicFields");

    // Create new div for the field group
    const newFieldDiv = document.createElement("div");
    newFieldDiv.classList.add("space-y-4", "w-96", "fund-field-group"); // Space between fields

    // Fund Type Field
    const fundTypeContainer = document.createElement("div");
    fundTypeContainer.classList.add("flex", "items-center", "space-x-4");

    fundTypeContainer.innerHTML = `
        <label for="fund_type${memberCounter}" class="w-1/4">Fund Type <span class="text-red-500">*</span></label>
        <div class="w-3/4">
            <input list="fund_type_options${memberCounter}" id="fund_type${memberCounter}" name="fund_type${memberCounter}" placeholder="Enter the type of fund" class="text-black w-full p-2 border rounded-md" required>
            <datalist id="fund_type_options${memberCounter}">
                <option value="Maasa Pirivu">
                <option value="Palli Fund">
                <option value="Marriage Fund">
                <option value="Marriage Hall">
                <option value="Donation">
                <option value="Madrassa">
                <option value="Others">
            </datalist>
        </div>
    `;

    // Description Field
    const descriptionContainer = document.createElement("div");
    descriptionContainer.classList.add("flex", "items-center", "space-x-4");

    descriptionContainer.innerHTML = `
        <label for="description${memberCounter}" class="w-1/4">Description</label>
        <input type="text" id="description${memberCounter}" name="description${memberCounter}" placeholder="Enter the Description" class="text-black w-3/4 p-2 border rounded-md">
    `;

    // Amount Field
    const amountContainer = document.createElement("div");
    amountContainer.classList.add("flex", "items-center", "space-x-4");

    amountContainer.innerHTML = `
        <label for="amount${memberCounter}" class="w-1/4">Amount <span class="text-red-500">*</span></label>
        <div class="flex items-center space-x-4">
        <input type="number" id="amount${memberCounter}" name="amount${memberCounter}" placeholder="Enter the amount" class="text-black w-3/4 p-2 border rounded-md amount-field" required>
        <button class="btn btn-error remove-btn" type="button">Remove</button>
        </div>
        
    `;

    // Append all containers to the newFieldDiv
    newFieldDiv.appendChild(fundTypeContainer);
    newFieldDiv.appendChild(descriptionContainer);
    newFieldDiv.appendChild(amountContainer);

    // Append the new field group to the dynamicFields container
    dynamicFields.appendChild(newFieldDiv);

    // Increment the counter for the next set of fields
    memberCounter++;

    // Add event listener to the new "Remove" button to delete the field
    const removeButton = newFieldDiv.querySelector(".remove-btn");
    removeButton.addEventListener("click", function() {
        // Remove the whole field group (newFieldDiv)
        newFieldDiv.remove();
    });

    // Add event listener to the new amount input
    const newAmountInput = newFieldDiv.querySelector(".amount-field");
    newAmountInput.addEventListener("input", updateTotalAmount);
});

// Pallipirivu Function to calculate and update the total amount
function updateTotalAmount() {
    const amountFields = document.querySelectorAll(".amount-field");
    let total = 0;

    amountFields.forEach((field) => {
        const value = parseFloat(field.value);
        console.log(`Field value: ${value}`);
        if (!isNaN(value)) {
            total += value;
        }
    });

    console.log(`Calculated Total: ${total}`);
    const totalAmountField = document.querySelector("#total_amount");
    if (totalAmountField) {
        totalAmountField.value = Math.round(total).toString(); // Remove decimals completely
        console.log(`Updated Total Amount Field: ${totalAmountField.value}`);
    } else {
        console.error("Total Amount field not found in DOM");
    }
}

// Add input event listener to all fields with the class "amount-field"
document.querySelectorAll(".amount-field").forEach((field) => {
    field.addEventListener("input", updateTotalAmount);
});





