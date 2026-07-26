/* -------------------------------------------------------------
   Water Purity Tracker - Frontend Rule Engine Real-Time Listener
   (rule_engine.js)
   ------------------------------------------------------------- */

document.addEventListener('DOMContentLoaded', () => {
  const phInput = document.getElementById('inputPh');
  const tdsInput = document.getElementById('inputTds');
  const turbidityInput = document.getElementById('inputTurbidity');
  const tempInput = document.getElementById('inputTemp');

  if (phInput && tdsInput && turbidityInput && tempInput) {
    const inputs = [phInput, tdsInput, turbidityInput, tempInput];
    inputs.forEach(input => {
      input.addEventListener('input', debounce(triggerLiveAnalysis, 300));
    });

    // Run initial preview
    triggerLiveAnalysis();
  }
});

async function triggerLiveAnalysis() {
  const ph = parseFloat(document.getElementById('inputPh').value) || 7.0;
  const tds = parseFloat(document.getElementById('inputTds').value) || 300;
  const turbidity = parseFloat(document.getElementById('inputTurbidity').value) || 1.0;
  const temp = parseFloat(document.getElementById('inputTemp').value) || 25.0;

  try {
    const res = await fetch('/api/analyze', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ ph, tds, turbidity, temperature: temp })
    });

    const data = await res.json();
    updateLivePreviewUI(data);
  } catch (err) {
    console.error("Live analysis preview error:", err);
  }
}

function updateLivePreviewUI(data) {
  const scoreEl = document.getElementById('liveScoreNumber');
  const statusEl = document.getElementById('liveStatusBadge');
  const recEl = document.getElementById('liveRecommendationText');
  const circleBar = document.getElementById('liveScoreCircleBar');

  if (scoreEl) scoreEl.innerText = data.score;
  if (statusEl) {
    statusEl.innerText = data.status;
    statusEl.className = data.status === 'SAFE' ? 'status-badge safe' : 'status-badge unsafe';
  }

  if (recEl && data.ai_diagnosis) {
    recEl.innerText = data.ai_diagnosis.summary;
  }

  if (circleBar) {
    // 440 is stroke-dasharray max length
    const offset = 440 - (440 * data.score) / 100;
    circleBar.style.strokeDashoffset = offset;
    circleBar.setAttribute('class', `circular-score-bar ${data.status.toLowerCase()}`);
  }
}

function debounce(func, delay) {
  let timer;
  return function (...args) {
    clearTimeout(timer);
    timer = setTimeout(() => func.apply(this, args), delay);
  };
}
