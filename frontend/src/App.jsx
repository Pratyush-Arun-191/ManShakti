const API_BASE_URL = "https://manshakti-backend.onrender.com";
import { useState } from "react";
import "./App.css";

function App() {
  const [activeModule, setActiveModule] = useState("wellbeing");

  return (
    <div className="app">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-icon">M</div>
          <div>
            <h1>ManShakti</h1>
            <p>Student Insight Platform</p>
          </div>
        </div>

        <div className="nav-section">
          <p className="nav-label">STUDENT</p>

          <button
            className={`nav-item ${
              activeModule === "wellbeing" ? "active" : ""
            }`}
            onClick={() => setActiveModule("wellbeing")}
          >
            <span>◉</span>
            Wellbeing
          </button>

          <button
            className={`nav-item ${
              activeModule === "academic" ? "active" : ""
            }`}
            onClick={() => setActiveModule("academic")}
          >
            <span>▣</span>
            Academic
          </button>
        </div>

        <div className="nav-section">
          <p className="nav-label">FACULTY</p>

          <button
            className={`nav-item ${
              activeModule === "teacher" ? "active" : ""
            }`}
            onClick={() => setActiveModule("teacher")}
          >
            <span>◈</span>
            Teacher Insights
          </button>
        </div>

        <div className="sidebar-bottom">
          <div className="student-card">
            <div className="avatar">DS</div>
            <div>
              <strong>Demo Student</strong>
              <p>AI006</p>
            </div>
          </div>
        </div>
      </aside>

      <main className="main-content">
        <header className="topbar">
          <div>
            <p className="eyebrow">
              {activeModule === "teacher"
                ? "TEACHER DASHBOARD"
                : "STUDENT DASHBOARD"}
            </p>

            <h2>
              {activeModule === "wellbeing"
                ? "How are you feeling today?"
                : activeModule === "academic"
                ? "Check your understanding"
                : "Understand your class better"}
            </h2>
          </div>

          <div className="status">
            <span className="status-dot"></span>
            AI system online
          </div>
        </header>

        {activeModule === "wellbeing" ? (
          <Wellbeing />
        ) : activeModule === "academic" ? (
          <Academic />
        ) : (
          <Teacher />
        )}
      </main>
    </div>
  );
}

function Wellbeing() {
  const [reflection, setReflection] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  const submitReflection = async () => {
    if (!reflection.trim()) return;

    setLoading(true);
    setResult(null);
    setError("");

    try {
      const response = await fetch(`${API_BASE_URL}/reflection`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          student_roll_no: "AI006",
          text: reflection,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Something went wrong.");
      }

      if (data.already_submitted) {
        setError(data.message);
      } else {
        setResult(data);
        setReflection("");
      }
    } catch (err) {
      setError(
        err.message ||
          "Could not connect to the ManShakti backend."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="content">
      <div className="hero-card">
        <div>
          <span className="pill">DAILY CHECK-IN</span>
          <h3>Your voice matters.</h3>
          <p>
            Take a moment to describe how your day went. ManShakti analyzes
            your response for patterns that may need attention.
          </p>
        </div>

        <div className="hero-icon">♡</div>
      </div>

      <div className="section-header">
        <div>
          <h3>Today's reflection</h3>
          <p>Share honestly. There are no right or wrong answers.</p>
        </div>

        <span className="date-label">Daily response</span>
      </div>

      <div className="reflection-card">
        <textarea
          value={reflection}
          onChange={(e) => setReflection(e.target.value)}
          placeholder="How was your day today? You can talk about classes, assignments, friends, future plans, or anything that affected you..."
          disabled={loading}
        />

        <div className="form-footer">
          <span>{reflection.length} characters</span>

          <button
            className="primary-button"
            disabled={!reflection.trim() || loading}
            onClick={submitReflection}
          >
            {loading ? "Analyzing..." : "Analyze my reflection →"}
          </button>
        </div>
      </div>

      {error && (
        <div className="result-card error-card">
          <h4>{error}</h4>
        </div>
      )}

      {result && (
        <div className="result-card">
          <div className="result-header">
            <div>
              <span className="result-label">AI ANALYSIS</span>
              <h3>Here's what ManShakti found</h3>
            </div>

            <div className="stress-badge">
              Stress level: {result.stress_level}
            </div>
          </div>

          <div className="result-section">
            <span>INDICATOR</span>
            <strong>{result.indicator}</strong>
          </div>

          <div className="result-section">
            <span>SUMMARY</span>
            <p>{result.summary}</p>
          </div>

          <div className="history-box">
            <div>
              <span>Recent concerning days</span>
              <strong>
                {result.history_analysis.concerning_days}
              </strong>
            </div>

            <div>
              <span>Support alert</span>
              <strong>
                {result.history_analysis.alert ? "Triggered" : "Not triggered"}
              </strong>
            </div>
          </div>
        </div>
      )}

      <div className="info-grid">
        <div className="info-card">
          <span className="info-icon">✦</span>
          <div>
            <h4>AI-powered analysis</h4>
            <p>
              Your reflection is converted into structured wellbeing
              indicators.
            </p>
          </div>
        </div>

        <div className="info-card">
          <span className="info-icon">◷</span>
          <div>
            <h4>Pattern, not one day</h4>
            <p>
              ManShakti considers recent history instead of reacting to a
              single difficult day.
            </p>
          </div>
        </div>
      </div>
    </section>
  );
}

function Academic() {
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  const question =
    "Explain the difference between supervised and unsupervised learning.";

  const evaluateAnswer = async () => {
    if (!answer.trim()) return;

    setLoading(true);
    setResult(null);
    setError("");

    try {
      const response = await fetch(`${API_BASE_URL}/academic/evaluate`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            student_roll_no: "AI006",
            question: question,
            answer: answer,
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Something went wrong.");
      }

      setResult(data);
    } catch (err) {
      setError(
        err.message || "Could not connect to the ManShakti backend."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="content">
      <div className="hero-card academic-hero">
        <div>
          <span className="pill">ACADEMIC UNDERSTANDING</span>
          <h3>Show what you understand.</h3>
          <p>
            Write your answer naturally. AI will identify what you understand
            and where a concept may need more attention.
          </p>
        </div>

        <div className="hero-icon">⌁</div>
      </div>

      <div className="question-card">
        <span className="question-label">SUBJECTIVE QUESTION</span>

        <h3>{question}</h3>

        <p className="question-help">
          Explain the concept in your own words and give an example of each.
        </p>

        <textarea
          value={answer}
          onChange={(e) => setAnswer(e.target.value)}
          placeholder="Write your answer here..."
          disabled={loading}
        />

        <div className="form-footer">
          <span>{answer.length} characters</span>

          <button
            className="primary-button"
            disabled={!answer.trim() || loading}
            onClick={evaluateAnswer}
          >
            {loading ? "Evaluating..." : "Evaluate answer →"}
          </button>
        </div>
      </div>

      {error && (
        <div className="result-card error-card">
          <h4>{error}</h4>
        </div>
      )}

      {result && (
        <div className="result-card academic-result">
          <div className="result-header">
            <div>
              <span className="result-label">AI EVALUATION</span>
              <h3>Your understanding</h3>
            </div>

            <div className="understanding-badge">
              {result.understanding}
            </div>
          </div>

          <div className="result-section">
            <span>CONCEPT GAP</span>
            <strong>{result.missing_concept}</strong>
          </div>

          <div className="result-section">
            <span>FEEDBACK</span>
            <p>{result.feedback}</p>
          </div>

          <div className="resource-box">
            <div>
              <span>RECOMMENDED LEARNING TOPIC</span>
              <strong>{result.resource_query}</strong>
            </div>

            <a
              href={`https://www.google.com/search?q=${encodeURIComponent(
                result.resource_query
              )}`}
              target="_blank"
              rel="noreferrer"
            >
              Find resources →
            </a>
          </div>
        </div>
      )}
    </section>
  );
}

function Teacher() {
  const students = [
    {
      roll: "AI006",
      name: "Demo Student",
      academic: "Strong",
      concept: "No major concept gap identified",
      indicator: "academic pressure",
      concerningDays: 2,
      attention: false,
    },
    {
      roll: "AI005",
      name: "Student 2",
      academic: "Partial",
      concept: "Understanding of model evaluation needs improvement",
      indicator: "future career concern",
      concerningDays: 3,
      attention: true,
    },
    {
      roll: "AI004",
      name: "Student 3",
      academic: "Weak",
      concept: "Confusion between supervised and unsupervised learning",
      indicator: "No clear concern",
      concerningDays: 1,
      attention: false,
    },
  ];

  return (
    <section className="content">
      <div className="hero-card">
        <div>
          <span className="pill">TEACHER INSIGHTS</span>
          <h3>Understand your class better.</h3>
          <p>
            ManShakti brings academic understanding and wellbeing indicators
            together so teachers can identify where students may need support.
          </p>
        </div>
        <div className="hero-icon">◈</div>
      </div>

      <div className="section-header">
        <div>
          <h3>Class overview</h3>
          <p>AI-generated insights from recent student activity.</p>
        </div>
        <span className="date-label">3 students</span>
      </div>

      <div className="teacher-stats">
        <div className="stat-card">
          <span>STUDENTS ANALYZED</span>
          <strong>3</strong>
        </div>

        <div className="stat-card">
          <span>NEED ACADEMIC ATTENTION</span>
          <strong>2</strong>
        </div>

        <div className="stat-card">
          <span>WELLBEING ALERTS</span>
          <strong>1</strong>
        </div>
      </div>

      <div className="student-table-card">
        <div className="table-header">
          <div>
            <h3>Student insights</h3>
            <p>Review patterns and decide where human support is needed.</p>
          </div>
        </div>

        <div className="student-list">
          {students.map((student) => (
            <div className="student-row" key={student.roll}>
              <div className="student-info">
                <div className="student-avatar">
                  {student.name.charAt(0)}
                </div>

                <div>
                  <strong>{student.name}</strong>
                  <span>{student.roll}</span>
                </div>
              </div>

              <div className="student-field">
                <span>ACADEMIC</span>
                <strong className={`status-${student.academic.toLowerCase()}`}>
                  {student.academic}
                </strong>
              </div>

              <div className="student-field">
                <span>CONCEPT GAP</span>
                <strong>{student.concept}</strong>
              </div>

              <div className="student-field">
                <span>WELLBEING INDICATOR</span>
                <strong>{student.indicator}</strong>
              </div>

              <div className="student-field">
                <span>RECENT PATTERN</span>
                <strong>
                  {student.concerningDays} concerning days
                </strong>
              </div>

              <div>
                {student.attention ? (
                  <span className="attention-badge">
                    Review
                  </span>
                ) : (
                  <span className="normal-badge">
                    Monitor
                  </span>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="teacher-note">
        <span>HUMAN-IN-THE-LOOP</span>
        <p>
          These insights are intended to support teacher review, not replace
          professional judgment. ManShakti highlights patterns so educators
          can decide when further support may be appropriate.
        </p>
      </div>
    </section>
  );
}

export default App;