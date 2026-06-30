const API_URL = "http://127.0.0.1:5000";

async function getCurrentTab() {
  const tabs = await chrome.tabs.query({ active: true, currentWindow: true });
  return tabs[0];
}

async function loadCurrentPageInfo() {
  const tab = await getCurrentTab();

  document.getElementById("name").value = tab.title || "Unknown Product";

  return {
    title: tab.title || "Unknown Product",
    url: tab.url
  };
}

async function trackProduct() {
  const status = document.getElementById("status");
  const nameInput = document.getElementById("name");
  const targetInput = document.getElementById("targetPrice");

  status.textContent = "Adding product...";

  const tab = await getCurrentTab();
  const targetPrice = targetInput.value;

  if (!targetPrice) {
    status.textContent = "Please enter a target price.";
    return;
  }

  try {
    const response = await fetch(`${API_URL}/api/products`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        name: nameInput.value || tab.title || "Unknown Product",
        url: tab.url,
        target_price: Number(targetPrice)
      })
    });

    const data = await response.json();

    if (!response.ok) {
      status.textContent = data.error || "Could not add product.";
      return;
    }

    status.textContent = "Product added!";
  } catch (error) {
    status.textContent = "API not running. Start python api.py first.";
  }
}

function openDashboard() {
  chrome.tabs.create({ url: `${API_URL}/` });
}

document.getElementById("trackBtn").addEventListener("click", trackProduct);
document.getElementById("dashboardBtn").addEventListener("click", openDashboard);

loadCurrentPageInfo();
