let memberCounter = 1; // Counter for unique 'name' attributes

document.getElementById("addOptionButton").addEventListener("click", function () {
    const dynamicFields = document.getElementById("dynamicFields");

    const newField = document.createElement("div");
    newField.classList.add("flex", "items-center", "space-x-4", "w-96");

    newField.innerHTML = `
        <label for="family_member${memberCounter}" class="w-1/4">Family Member<span class="text-red-500">*</span></label>
        <div class="w-3/4 space-y-4">
            <input id="family_member${memberCounter}" name="family_member${memberCounter}" placeholder="Family Member Name" class="text-black w-full p-2 border rounded-md">
            <input list="relation_list" id="relation${memberCounter}" name="relation${memberCounter}" placeholder="Relation" class="text-black w-full p-2 border rounded-md">
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

    dynamicFields.appendChild(newField);

    // Increment the counter for the next set of fields
    memberCounter++;
});
