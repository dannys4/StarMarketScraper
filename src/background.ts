// Listen for clicks on the extension icon
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.type === "download") {
        const { object, filename } = message.payload;
        const blob = new Blob([JSON.stringify(object)], { type: "application/json;charset=utf-8" });
        var reader = new FileReader();
        reader.readAsDataURL(blob);
        reader.onload = function () {
            const dataUrl = reader.result?.toString();
            if (!dataUrl) {
                console.error('Could not generate data URL');
                return;
            }
            chrome.downloads.download({
                url: dataUrl,
                filename,
                saveAs: true
            }, (downloadId) => {
                if (chrome.runtime.lastError) {
                    console.error("Download failed:", chrome.runtime.lastError.message);
                } else {
                    console.log("Download started with ID:", downloadId);
                }
            });
        };
    }
});

chrome.action.onClicked.addListener((tab) => {
    chrome.scripting.executeScript({
        target: { tabId: tab.id ? tab.id : -1 }, // Target the specific tab where the icon was clicked
        func: saveItemDetails // Run the function to save item details
    }).then(() => {
        console.log('Item details collected and processed.');
    });
});



function saveItemDetails() {

    function collectItemDetails() {
        const items = document.querySelectorAll('.Item_subItemContent__tmnap'); // Select all divs with class Item_subItemContent__tmnap

        if (items.length === 0) {
            console.log('No items found on the page.');
            return null;
        }

        const itemList: { name: string; quantity: string; price: string }[] = [];
        items.forEach((item) => {
            // Collect contents in subdiv that has class name with substring "itemName"
            const itemName = item.querySelector('[class*="itemName"]')?.textContent?.trim();
            const itemQty = item.querySelector('[class*="itemQty"]')?.textContent?.trim();
            const price = item.querySelector('[class*="price"]')?.textContent?.trim();
            if (itemName && itemQty && price) {
                itemList.push({ name: itemName, quantity: itemQty, price });
            }
        });

        return itemList;
    }
    function getListDate() {
            const dateString = document.querySelector('[class*="orderDateString"]')?.textContent?.trim();
            if (!dateString) {
                return;
            }
            const dateObj = new Date(Date.parse(dateString));
            const options: Intl.DateTimeFormatOptions = { year: 'numeric', month: '2-digit', day: '2-digit' };
            const dateStringFormat = dateObj.toLocaleString('en-US', options);
            // Replace slash with dash
            const dateStringDash = "-" + dateStringFormat.replace(/\//g, '-');
            console.log(dateString);
            console.log(dateObj);
            console.log(dateStringFormat);
            console.log(dateStringDash);
            return dateStringDash;
    }
    let date = getListDate();
    if (!date) {
        console.warn('Date not found! Omitting...');
        date = "";
    }
    const itemList = collectItemDetails();

    if (!itemList || itemList.length === 0) {
        console.log('No items found on the page or list is empty.');
        return;
    }

    console.log(itemList);

    // Create a Blob object containing the JSON data
    chrome.runtime.sendMessage({
        type: "download",
        payload: {
            object: itemList,
            filename: "item-details" + date + ".json"
        }
    });
}
