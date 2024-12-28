document.addEventListener("DOMContentLoaded", function () {
    const balanceField = document.getElementById("balance");
    console.log("Raw balance dataset:", balanceField.dataset.balance);

    const balanceData = JSON.parse(balanceField.dataset.balance || "[]");
    console.log("Parsed balance data:", balanceData);

    if (balanceData.length > 0 && balanceData[0].balance) {
        balanceField.value = balanceData[0].balance; // Set balance if present
        console.log("Balance set to:", balanceField.value);
    } else {
        balanceField.value = "0"; // Default to 0
        console.log("Balance defaulted to 0");
    }
});
