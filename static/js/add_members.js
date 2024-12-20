let memberCounter = 1; // Counter for unique 'name' attributes

document.getElementById("addOptionButton").addEventListener("click", function () {
    const dynamicFields = document.getElementById("dynamicFields");

    // Create the container for a new dynamic field
    const newField = document.createElement("div");
    newField.classList.add("flex", "items-center", "space-x-4", "w-96");
    newField.setAttribute("id", `field-${memberCounter}`); // Assign a unique ID to the field

    // Create the content of the dynamic field
    newField.innerHTML = `
        <label for="family_member${memberCounter}" class="w-1/4">Family Member<span class="text-red-500">*</span></label>
        <div class="w-3/4 space-y-4">
            <input id="family_member" name="family_member" placeholder="Family Member Name" 
                   class="text-black w-full p-2 border rounded-md">
            <div class="flex items-center space-x-4">
                <input list="relation_list" id="relation" name="relation" placeholder="Relation" 
                       class="text-black w-full p-2 border rounded-md">
                <button class="btn btn-error remove-btn" type="button">Remove</button>
            </div>
            <datalist id="relation_list">
                <option value="Mother">
                <option value="Father">
                <option value="Grand Father">
                <option value="Grand Mother">
                <option value="Wife">
                <option value="Son">
                <option value="Daughter">
                <option value="Brother">
                <option value="Sister">
                <option value="Cousin">
            </datalist>
        </div>
    `;

    // Add the new field to the dynamic fields container
    dynamicFields.appendChild(newField);

    // Attach event listener to the Remove button
    const removeButton = newField.querySelector(".remove-btn");
    removeButton.addEventListener("click", function () {
        dynamicFields.removeChild(newField); // Remove the field when the button is clicked
    });

    // Increment the counter for the next set of fields
    memberCounter++;
});
