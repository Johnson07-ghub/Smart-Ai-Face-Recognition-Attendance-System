let stream = null;

// OPTIONAL: if you still use <video> element
let video = document.getElementById("video");

// ===============================
// START CAMERA (ONLY FOR LOCAL PREVIEW)
// ===============================
function startCamera() {
    navigator.mediaDevices.getUserMedia({ video: true })
    .then(s => {
        stream = s;

        if (video) {
            video.srcObject = stream;
            video.play();
        }

        document.getElementById("result").innerHTML =
            "📷 Camera started successfully";
    })
    .catch(err => {
        alert("Camera error: " + err.message);
    });
}

// ===============================
// START ATTENDANCE (AI STREAM MODE)
// ===============================
function startAttendance() {

    // Redirect to live AI camera page
    window.location = "/";

}

// ===============================
// VIEW DASHBOARD
// ===============================
function viewAttendance() {
    window.location = "/dashboard";
}

// ===============================
// STATUS UPDATE (OPTIONAL UI FEEDBACK)
// ===============================
function showStatus(message, type = "success") {

    const result = document.getElementById("result");

    if (!result) return;

    result.innerHTML = `
        <span class="badge bg-${type}">
            ${message}
        </span>
    `;
}