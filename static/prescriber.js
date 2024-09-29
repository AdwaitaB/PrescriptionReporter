let currentPatient = null;

// DOM elements
const addPatientForm = document.getElementById('add-patient-form');
const searchInput = document.getElementById('search-input');
const searchResults = document.getElementById('search-results');
const backBtn = document.getElementById('back-btn');
const scheduleAppointmentBtn = document.getElementById('schedule-appointment');

// Event listeners
searchInput.addEventListener('input', handleSearch);
backBtn.addEventListener('click', () => showPage('home-page'));
scheduleAppointmentBtn.addEventListener('click', handleScheduleAppointment);

// Navigation
document.querySelectorAll('nav a').forEach(link => {
  link.addEventListener('click', (e) => {
    e.preventDefault();
    renderPatientLists()
    showPage(e.target.getAttribute('href').slice(1));
  });
});

// Add patient handler
function handleAddPatient(e) {
  e.preventDefault();
  const formData = new FormData(addPatientForm);
  const newPatient = {
    id: patients.length + 1,
    name: formData.get('patient-name'),
    age: parseInt(formData.get('patient-age')),
    gender: formData.get('patient-gender'),
    severity: parseInt(formData.get('patient-severity')),
    records: formData.get('patient-records').split(','),
    medicineHistory: formData.get('patient-medicine').split(','),
    familyHistory: formData.get('patient-family-history'),
    allergies: formData.get('patient-allergies'),
    bloodType: formData.get('patient-blood-type'),
    healthData: [80, 82, 81, 83, 85] // Default health data
  };
  patients.push(newPatient);
  renderDashboard();
  addPatientForm.reset();
  showPage('home-page');
}

// Search handler
function handleSearch(e) {
  const query = e.target.value.toLowerCase();
  const results = patients.filter(patient => 
    patient.name.toLowerCase().includes(query) ||
    patient.records.some(record => record.toLowerCase().includes(query)) ||
    patient.medicineHistory.some(medicine => medicine.toLowerCase().includes(query))
  );
  renderSearchResults(results);
}

// Render dashboard
function renderDashboard() {
  renderPatientLists();
  updateDashboardSummary();
}

// Render patient lists
function renderPatientLists() {
  const criticalList = document.getElementById('critical-patient-list');
  const moderateList = document.getElementById('moderate-patient-list');
  const stableList = document.getElementById('stable-patient-list');

  criticalList.innerHTML = '';
  moderateList.innerHTML = '';
  stableList.innerHTML = '';

  patients.forEach((patient) => {
    const listItem = document.createElement('li');
    listItem.textContent = `${patient.name} (Severity: ${patient.severity})`;
    listItem.addEventListener('click', () => showPatientProfile(patient));

    if (patient.severity >= 8) {
      criticalList.appendChild(listItem);
    } else if (patient.severity >= 4) {
      moderateList.appendChild(listItem);
    } else {
      stableList.appendChild(listItem);
    }
  });
}

// Update dashboard summary
function updateDashboardSummary() {
  document.getElementById('total-patients').textContent = patients.length;
  document.getElementById('critical-cases').textContent = patients.filter(p => p.severity >= 8).length;
  const averageScore = patients.reduce((sum, p) => sum + p.severity, 0) / patients.length;
  document.getElementById('average-health-score').textContent = averageScore.toFixed(1);
}

// Show patient profile
function showPatientProfile(patient) {
  currentPatient = patient;
  showPage('patient-profile-page');
  document.getElementById('patient-name').textContent = patient.name;
  document.getElementById('patient-details').textContent = `Age: ${patient.age}, Gender: ${patient.gender}, Blood Type: ${patient.bloodType}`;
  document.getElementById('patient-severity-indicator').textContent = patient.severity;
  document.getElementById('patient-severity-indicator').style.color = getSeverityColor(patient.severity);
  document.getElementById('patient-records').innerHTML = patient.records.map(record => `<li>${record}</li>`).join('');
  document.getElementById('patient-medicine-history').innerHTML = patient.medicineHistory.map(medicine => `<li>${medicine}</li>`).join('');
  document.getElementById('patient-family-history').textContent = patient.familyHistory;
  document.getElementById('patient-allergies').textContent = patient.allergies;
  renderHealthChart(patient);
  renderAppointments(patient);
}

// Render health chart
function renderHealthChart(patient) {
  const ctx = document.getElementById('health-chart').getContext('2d');
  new Chart(ctx, {
    type: 'line',
    data: {
      labels: ['Week 1', 'Week 2', 'Week 3', 'Week 4', 'Week 5'],
      datasets: [{
        label: 'Health Score',
        data: patient.healthData,
        borderColor: 'rgb(75, 192, 192)',
        tension: 0.1
      }]
    },
    options: {
      responsive: true,
      scales: {
        y: {
          beginAtZero: true,
          max: 100
        }
      }
    }
  });
}

// Get severity color
function getSeverityColor(severity) {
  if (severity >= 8) return '#e74c3c';
  if (severity >= 4) return '#f39c12';
  return '#2ecc71';
}

// Show page
function showPage(pageId) {
  document.querySelectorAll('.page').forEach(page => {
    page.classList.toggle('active-page', page.id === pageId);
  });
  if (pageId === 'analytics-page') {
    renderAnalyticsCharts();
  }
}

// Render search results
function renderSearchResults(results) {
  searchResults.innerHTML = '';
  results.forEach(patient => {
    const resultItem = document.createElement('div');
    resultItem.classList.add('search-result');
    resultItem.textContent = patient.name;
    resultItem.addEventListener('click', () => showPatientProfile(patient));
    searchResults.appendChild(resultItem);
  });
}

// Handle schedule appointment
function handleScheduleAppointment() {
  if (currentPatient) {
    const date = document.getElementById('appointment-date').value;
    const time = document.getElementById('appointment-time').value;
    if (date && time) {
      currentPatient.appointments = currentPatient.appointments || [];
      currentPatient.appointments.push({ date, time });
      renderAppointments(currentPatient);
    } else {
      alert('Please select both date and time for the appointment.');
    }
  }
}

// Render appointments
function renderAppointments(patient) {
  const appointmentsList = document.getElementById('patient-appointments');
  appointmentsList.innerHTML = '';
  if (patient.appointments && patient.appointments.length > 0) {
    patient.appointments.forEach(appointment => {
      const appointmentItem = document.createElement('li');
      appointmentItem.textContent = `${appointment.date} at ${appointment.time}`;
      appointmentsList.appendChild(appointmentItem);
    });
  } else {
    appointmentsList.innerHTML = '<li>No appointments scheduled</li>';
  }
}

// Render analytics charts
function renderAnalyticsCharts() {
  renderAgeDistributionChart();
  renderSeverityDistributionChart();
  renderGenderDistributionChart();
  renderBloodTypeDistributionChart();
}

// Render age distribution chart
function renderAgeDistributionChart() {
  const ageGroups = {
    '0-20': 0, '21-40': 0, '41-60': 0, '61+': 0
  };
  patients.forEach(patient => {
    if (patient.age <= 20) ageGroups['0-20']++;
    else if (patient.age <= 40) ageGroups['21-40']++;
    else if (patient.age <= 60) ageGroups['41-60']++;
    else ageGroups['61+']++;
  });
  renderPieChart('age-distribution-chart', 'Age Distribution', ageGroups);
}

// Render severity distribution chart
function renderSeverityDistributionChart() {
  const severityGroups = {
    'Critical (8-10)': 0, 'Moderate (4-7)': 0, 'Stable (1-3)': 0
  };
  patients.forEach(patient => {
    if (patient.severity >= 8) severityGroups['Critical (8-10)']++;
    else if (patient.severity >= 4) severityGroups['Moderate (4-7)']++;
    else severityGroups['Stable (1-3)']++;
  });
  renderBarChart('severity-distribution-chart', 'Severity Distribution', severityGroups);
}

// Render gender distribution chart
function renderGenderDistributionChart() {
  const genderCount = {
    Male: patients.filter(p => p.gender === 'male').length,
    Female: patients.filter(p => p.gender === 'female').length,
    Other: patients.filter(p => p.gender === 'other').length
  };
  renderPieChart('gender-distribution-chart', 'Gender Distribution', genderCount);
}

// Render blood type distribution chart
function renderBloodTypeDistributionChart() {
  const bloodTypeCount = {};
  patients.forEach(patient => {
    bloodTypeCount[patient.bloodType] = (bloodTypeCount[patient.bloodType] || 0) + 1;
  });
  renderPieChart('blood-type-distribution-chart', 'Blood Type Distribution', bloodTypeCount);
}

// Render pie chart
function renderPieChart(elementId, title, data) {
  const ctx = document.getElementById(elementId).getContext('2d');
  new Chart(ctx, {
    type: 'pie',
    data: {
      labels: Object.keys(data),
      datasets: [{
        data: Object.values(data),
        backgroundColor: ['#3498db', '#2ecc71', '#f1c40f', '#e74c3c', '#9b59b6', '#34495e', '#1abc9c', '#d35400']
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: { position: 'top' },
        title: { display: true, text: title }
      }
    }
  });
}

// Render bar chart
function renderBarChart(elementId, title, data) {
  const ctx = document.getElementById(elementId).getContext('2d');
  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: Object.keys(data),
      datasets: [{
        label: 'Number of Patients',
        data: Object.values(data),
        backgroundColor: ['#e74c3c', '#f39c12', '#2ecc71']
      }]
    },
    options: {
      responsive: true,
      scales: { y: { beginAtZero: true, stepSize: 1 } },
      plugins: {
        legend: { display: false },
        title: { display: true, text: title }
      }
    }
  });
}

function init() {
  renderDashboard();
}
