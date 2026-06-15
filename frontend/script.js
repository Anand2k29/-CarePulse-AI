/* ==========================================================================
   CarePulse AI Frontend JavaScript Logic Engine
   ========================================================================== */

const BACKEND_URL = "http://127.0.0.1:8000";

// DOM Elements
const statusDot = document.getElementById("statusDot");
const statusText = document.getElementById("statusText");
const chatForm = document.getElementById("chatForm");
const messageInput = document.getElementById("messageInput");
const chatMessages = document.getElementById("chatMessages");
const sendBtn = document.getElementById("sendBtn");

// Diagnostics Elements
const emptyState = document.getElementById("emptyState");
const diagnosticsContent = document.getElementById("diagnosticsContent");
const possibleCondition = document.getElementById("possibleCondition");
const conditionDescription = document.getElementById("conditionDescription");
const confidenceBadge = document.getElementById("confidenceBadge");
const matchedSymptoms = document.getElementById("matchedSymptoms");
const riskBadge = document.getElementById("riskBadge");
const severityScore = document.getElementById("severityScore");
const severityProgress = document.getElementById("severityProgress");
const severityPercent = document.getElementById("severityPercent");
const probabilityChart = document.getElementById("probabilityChart");
const precautionsList = document.getElementById("precautionsList");
const followUpChips = document.getElementById("followUpChips");
const emergencyOverlay = document.getElementById("emergencyOverlay");
const emergencySymptoms = document.getElementById("emergencySymptoms");
const dismissEmergencyBtn = document.getElementById("dismissEmergencyBtn");

// Circle properties for Progress Ring (r=34, circumference = 2 * PI * r = 213.628)
const CIRCUMFERENCE = 213.628;
severityProgress.style.strokeDasharray = `${CIRCUMFERENCE} ${CIRCUMFERENCE}`;
severityProgress.style.strokeDashoffset = CIRCUMFERENCE;

// Initialize connection check
async function checkBackendStatus() {
    try {
        const response = await fetch(`${BACKEND_URL}/`);
        if (response.ok) {
            statusDot.className = "status-dot online";
            statusText.textContent = "Online";
        } else {
            throw new Error("Offline Status Code");
        }
    } catch (error) {
        statusDot.className = "status-dot offline";
        statusText.textContent = "Offline (Check Server)";
        console.error("Connection check failed:", error);
    }
}

// Set circular progress bar offset
function setSeverityProgress(score) {
    // We assume 30 is the logical maximum severity score for the circular dial display
    const maxLogicalScore = 30;
    const percentage = Math.min(Math.round((score / maxLogicalScore) * 100), 100);
    const offset = CIRCUMFERENCE - (percentage / 100) * CIRCUMFERENCE;
    severityProgress.style.strokeDashoffset = offset;
    severityPercent.textContent = `${percentage}%`;
    
    // Change progress ring color based on risk
    if (score >= 15) {
        severityProgress.style.stroke = "#ef4444"; // Red
    } else if (score >= 7) {
        severityProgress.style.stroke = "#f59e0b"; // Yellow
    } else {
        severityProgress.style.stroke = "#10b981"; // Green
    }
}

// Render message bubbles in chat thread
function appendMessage(sender, text, isHtml = false) {
    const messageDiv = document.createElement("div");
    messageDiv.className = `message ${sender}-message fade-in`;
    
    const avatarIcon = sender === "user" ? "fa-user" : "fa-robot";
    const avatarHtml = `<div class="message-avatar"><i class="fa-solid ${avatarIcon}"></i></div>`;
    
    const timeString = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    
    const contentHtml = `
        <div class="message-content">
            <p>${isHtml ? text : escapeHTML(text)}</p>
            <span class="message-time">${timeString}</span>
        </div>
    `;
    
    messageDiv.innerHTML = sender === "user" ? contentHtml + avatarHtml : avatarHtml + contentHtml;
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Escapes special characters for safety in text output
function escapeHTML(str) {
    return str.replace(/[&<>'"]/g, 
        tag => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;' }[tag] || tag)
    );
}

// Append typing animation loader bubble
function appendTypingIndicator() {
    const indicatorDiv = document.createElement("div");
    indicatorDiv.id = "typingIndicator";
    indicatorDiv.className = "message system-message fade-in";
    indicatorDiv.innerHTML = `
        <div class="message-avatar"><i class="fa-solid fa-robot"></i></div>
        <div class="message-content">
            <div class="typing-indicator">
                <span class="typing-dot"></span>
                <span class="typing-dot"></span>
                <span class="typing-dot"></span>
            </div>
        </div>
    `;
    chatMessages.appendChild(indicatorDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Remove typing animation loader bubble
function removeTypingIndicator() {
    const indicator = document.getElementById("typingIndicator");
    if (indicator) {
        indicator.remove();
    }
}

// Update the right diagnostics panel with API data
function updateDiagnosticsDashboard(data) {
    // 1. Unhide panel
    emptyState.classList.add("hidden");
    diagnosticsContent.classList.remove("hidden");
    emergencyOverlay.classList.add("hidden");

    // 2. Main Condition Overview
    possibleCondition.textContent = data.Possible_Condition;
    conditionDescription.textContent = data.Description;
    confidenceBadge.textContent = `${data.Confidence_percent}% Match`;

    // 3. Matched Symptoms
    matchedSymptoms.innerHTML = "";
    data.Matched_Symptoms.forEach(symptom => {
        const span = document.createElement("span");
        span.className = "symptom-tag";
        span.textContent = symptom;
        matchedSymptoms.appendChild(span);
    });

    // 4. Severity Circular Progress
    severityScore.textContent = data.Severity_Score;
    setSeverityProgress(data.Severity_Score);

    // 5. Risk Badge Class mapping
    riskBadge.textContent = data.Risk_Level;
    riskBadge.className = "risk-badge"; // reset classes
    if (data.Risk_Level === "High") {
        riskBadge.classList.add("high");
    } else if (data.Risk_Level === "Medium") {
        riskBadge.classList.add("medium");
    } else {
        riskBadge.classList.add("low");
    }

    // 6. Top 3 predictions bars
    probabilityChart.innerHTML = "";
    data.Top_3_Predictions.forEach(pred => {
        const item = document.createElement("div");
        item.className = "chart-item";
        item.innerHTML = `
            <div class="chart-item-header">
                <span class="chart-item-name">${pred.Disease}</span>
                <span class="chart-item-val">${pred.Probability_percent}%</span>
            </div>
            <div class="chart-bar-bg">
                <div class="chart-bar-fill" style="width: ${pred.Probability_percent}%"></div>
            </div>
        `;
        probabilityChart.appendChild(item);
    });

    // 7. Precautions Grid Cards
    precautionsList.innerHTML = "";
    data.Recommended_Precautions.forEach(prec => {
        const item = document.createElement("div");
        item.className = "precaution-item";
        item.innerHTML = `
            <i class="fa-solid fa-circle-check"></i>
            <span>${prec.charAt(0).toUpperCase() + prec.slice(1)}</span>
        `;
        precautionsList.appendChild(item);
    });

    // 8. Follow-up Questions Chips
    followUpChips.innerHTML = "";
    if (data.Follow_up_Questions && data.Follow_up_Questions.length > 0) {
        data.Follow_up_Questions.forEach(question => {
            const chip = document.createElement("div");
            chip.className = "follow-chip";
            chip.innerHTML = `
                <i class="fa-solid fa-plus"></i>
                <span>${question}</span>
            `;
            chip.addEventListener("click", () => {
                const messageText = `I am also experiencing ${question.toLowerCase()}`;
                messageInput.value = messageText;
                messageInput.focus();
            });
            followUpChips.appendChild(chip);
        });
        document.querySelector(".follow-up-card").classList.remove("hidden");
    } else {
        document.querySelector(".follow-up-card").classList.add("hidden");
    }
}

// Display Emergency Alert Interface
function triggerEmergencyUI(data) {
    emergencyOverlay.classList.remove("hidden");
    emergencySymptoms.innerHTML = "";
    
    // Add emergency symptoms tags
    data.Matched_Symptoms.forEach(s => {
        const span = document.createElement("span");
        span.className = "symptom-tag";
        span.textContent = s.replace("_", " ").toUpperCase();
        emergencySymptoms.appendChild(span);
    });
}

// Handle Form Submission
chatForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const text = messageInput.value.trim();
    if (!text) return;

    // Send user message
    appendMessage("user", text);
    messageInput.value = "";
    
    // Check Status
    checkBackendStatus();

    // Show indicator
    appendTypingIndicator();

    try {
        const response = await fetch(`${BACKEND_URL}/chat`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ message: text })
        });

        const data = await response.json();
        removeTypingIndicator();

        if (!response.ok) {
            // Display friendly API warning (e.g. no symptoms matched)
            const errorMsg = data.detail || "I could not identify any symptoms in your message. Could you please specify your symptoms (like fever, headache, stomach pain) more clearly?";
            appendMessage("system", errorMsg);
            return;
        }

        // Process Response
        if (data.Emergency) {
            triggerEmergencyUI(data);
            
            const alertText = `🚨 <strong>Emergency symptoms detected!</strong><br><br>The symptoms you described (${data.Matched_Symptoms.join(', ')}) suggest a potential emergency. <strong>Please seek immediate professional medical attention.</strong>`;
            appendMessage("system", alertText, true);
        } else {
            // Standard Condition
            const textResponse = `Based on your description, my primary match is <strong>${data.Possible_Condition}</strong> (Risk level: <strong>${data.Risk_Level}</strong>). <br><br><strong>Precautions advised:</strong><br>` + 
                data.Recommended_Precautions.map(p => `• ${p.charAt(0).toUpperCase() + p.slice(1)}`).join("<br>");
            
            appendMessage("system", textResponse, true);
            updateDiagnosticsDashboard(data);
        }

    } catch (error) {
        removeTypingIndicator();
        console.error("API error:", error);
        appendMessage("system", "Error: Unable to reach the diagnostic server. Please make sure the backend FastAPI application is running locally.");
        
        statusDot.className = "status-dot offline";
        statusText.textContent = "Offline (Check Server)";
    }
});

// Dismiss Emergency overlay
dismissEmergencyBtn.addEventListener("click", () => {
    emergencyOverlay.classList.add("hidden");
});

// Run startup check
checkBackendStatus();
setInterval(checkBackendStatus, 15000); // Poll every 15s
