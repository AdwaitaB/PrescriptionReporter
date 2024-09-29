const signupForm = document.getElementById('signup-form');
const patientInfo = document.getElementById('patient-info');
const questionnaire = document.getElementById('questionnaire');
const results = document.getElementById('results');
const questionText = document.getElementById('question-text');
const answerOptions = document.getElementById('answer-options');
const nextBtn = document.getElementById('next-btn');
const prevBtn = document.getElementById('prev-btn');
const progressBar = document.getElementById('progress');
const startQuestionnaireBtn = document.getElementById('start-questionnaire');
const retakeBtn = document.getElementById('retake-btn');

let currentQuestionIndex = 0;
let patientAnswers = [];

const healthQuestions = [
    "How would you rate your overall health?",
    "How satisfied are you with your exercise routine?",
    "How would you rate your diet?",
    "How would you rate your sleep quality?",
    "How often do you feel stressed?",
    "How would you rate your work-life balance?",
    "How satisfied are you with your social life?",
    "How would you rate your mental health?",
    "How often do you engage in activities you enjoy?",
    "How would you rate your energy levels throughout the day?",
    "How satisfied are you with your productivity?",
    "How would you rate your overall quality of life?"
];

signupForm.addEventListener('submit', handleSignup);
startQuestionnaireBtn.addEventListener('click', startQuestionnaire);
nextBtn.addEventListener('click', () => navigateQuestion(1));
prevBtn.addEventListener('click', () => navigateQuestion(-1));
retakeBtn.addEventListener('click', startQuestionnaire);

function handleSignup(e) {
    e.preventDefault();
    const name = document.getElementById('name').value;
    const patientId = 'P' + Math.floor(100000 + Math.random() * 900000);

    document.getElementById('patient-name').textContent = name;
    document.getElementById('patient-id').textContent = patientId;

    signupForm.parentElement.style.display = 'none';
    patientInfo.style.display = 'block';
}

function startQuestionnaire() {
    patientInfo.style.display = 'none';
    results.style.display = 'none';
    questionnaire.style.display = 'block';
    currentQuestionIndex = 0;
    patientAnswers = [];
    showQuestion(0);
}

function showQuestion(index) {
    questionText.textContent = healthQuestions[index];
    answerOptions.innerHTML = '';
    for (let i = 0; i <= 5; i++) {
        const button = document.createElement('button');
        button.textContent = i;
        button.addEventListener('click', () => selectAnswer(i));
        answerOptions.appendChild(button);
    }

    prevBtn.style.display = index === 0 ? 'none' : 'inline-block';
    nextBtn.textContent = index === healthQuestions.length - 1 ? 'Finish' : 'Next';
    updateProgressBar();
}

function selectAnswer(answer) {
    patientAnswers[currentQuestionIndex] = answer;
    document.querySelectorAll('#answer-options button').forEach(btn => {
        btn.classList.toggle('selected', parseInt(btn.textContent) === answer);
    });
}

function navigateQuestion(direction) {
    currentQuestionIndex += direction;
    if (currentQuestionIndex >= 0 && currentQuestionIndex < healthQuestions.length) {
        showQuestion(currentQuestionIndex);
    } else if (currentQuestionIndex === healthQuestions.length) {
        finishQuestionnaire();
    }
}

function updateProgressBar() {
    const progress = ((currentQuestionIndex + 1) / healthQuestions.length) * 100;
    progressBar.style.width = `${progress}%`;
}

function finishQuestionnaire() {
    questionnaire.style.display = 'none';
    results.style.display = 'block';
    
    const currentDate = new Date().toLocaleDateString();
    document.getElementById('last-test-date').textContent = currentDate;
    
    renderResultsChart();
}

function renderResultsChart() {
    const ctx = document.getElementById('results-chart').getContext('2d');
    new Chart(ctx, {
        type: 'radar',
        data: {
            labels: healthQuestions,
            datasets: [{
                label: 'Your Health Assessment',
                data: patientAnswers,
                fill: true,
                backgroundColor: 'rgba(74, 144, 226, 0.2)',
                borderColor: 'rgb(74, 144, 226)',
                pointBackgroundColor: 'rgb(74, 144, 226)',
                pointBorderColor: '#fff',
                pointHoverBackgroundColor: '#fff',
                pointHoverBorderColor: 'rgb(74, 144, 226)'
            }]
        },
        options: {
            elements: {
                line: {
                    borderWidth: 3
                }
            },
            scales: {
                r: {
                    angleLines: {
                        display: false
                    },
                    suggestedMin: 0,
                    suggestedMax: 5
                }
            }
        }
    });
}
