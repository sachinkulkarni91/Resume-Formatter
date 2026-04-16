import React, { useState } from 'react'
import './App.css'
import { FileUpload } from './FileUpload'
import { applySuggestions, formatFromParsed, prepareConversion } from './api'

export function App() {
  const [targetResume, setTargetResume] = useState(null)
  const [template, setTemplate] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [success, setSuccess] = useState(false)
  const [formattedFile, setFormattedFile] = useState(null)
  const [workflowData, setWorkflowData] = useState(null)
  const [suggestionDecisions, setSuggestionDecisions] = useState({})

  const handleTargetResumeSelect = (file) => {
    setTargetResume(file)
    setError(null)
    setFormattedFile(null)
    setSuccess(false)
    setWorkflowData(null)
    setSuggestionDecisions({})
  }

  const handleTemplateSelect = (file) => {
    setTemplate(file)
    setError(null)
    setFormattedFile(null)
    setSuccess(false)
  }

  const normalizeSuggestions = (payload) => {
    const list = payload?.suggestions || []
    if (!Array.isArray(list)) return []

    return list.map((item, index) => {
      if (typeof item === 'string') {
        return {
          id: `S${index + 1}`,
          section: 'general',
          title: `Suggestion ${index + 1}`,
          reason: item,
          suggested_text: item
        }
      }
      return {
        id: item.id || `S${index + 1}`,
        section: item.section || 'general',
        title: item.title || `Suggestion ${index + 1}`,
        reason: item.reason || 'Recommended improvement',
        suggested_text: item.suggested_text || ''
      }
    })
  }

  const handleAnalyze = async () => {
    if (!targetResume || !template) {
      setError('Please select both a target resume and a template')
      return
    }

    setLoading(true)
    setError(null)
    setSuccess(false)

    try {
      const data = await prepareConversion(targetResume)
      const normalized = normalizeSuggestions(data.suggestions)
      setWorkflowData({
        parsedResume: data.parsed_resume,
        suggestions: normalized,
        atsScore: data.suggestions?.ats_score || null
      })
      setSuggestionDecisions({})
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'Error analyzing resume')
      console.error('Error:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleDecision = (id, accepted) => {
    setSuggestionDecisions((prev) => ({ ...prev, [id]: accepted }))
  }

  const handleGenerate = async () => {
    if (!workflowData || !template) {
      setError('Please analyze resume first')
      return
    }

    setLoading(true)
    setError(null)
    setSuccess(false)

    try {
      const accepted = workflowData.suggestions.filter(s => suggestionDecisions[s.id] === true)
      const parsedToFormat = accepted.length > 0
        ? await applySuggestions(workflowData.parsedResume, accepted)
        : workflowData.parsedResume

      const formattedBlob = await formatFromParsed(parsedToFormat, template)
      const url = window.URL.createObjectURL(formattedBlob)
      setFormattedFile({ name: 'formatted_resume.docx', url })
      setSuccess(true)
    } catch (err) {
      if (err.response?.data instanceof Blob) {
        try {
          const errorText = await err.response.data.text()
          const parsedError = JSON.parse(errorText)
          setError(parsedError.detail || 'Error generating formatted resume')
        } catch {
          setError('Error generating formatted resume')
        }
      } else {
        setError(err.response?.data?.detail || err.message || 'Error generating formatted resume')
      }
      console.error('Error:', err)
    } finally {
      setLoading(false)
    }
  }

  const downloadFile = () => {
    if (formattedFile) {
      const link = document.createElement('a')
      link.href = formattedFile.url
      link.download = formattedFile.name
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
    }
  }

  return (
    <div className="app">
      <header className="header">
        <h1>Resume Formatter</h1>
        <p>Convert any resume to match your reference template format</p>
      </header>

      <div className="container">
        {error && (
          <div className="error-message">
            ❌ {error}
          </div>
        )}

        {success && (
          <div className="success-message">
            ✅ Resume formatted successfully!
          </div>
        )}

        <div className="formatter-section">
          <div className="upload-section">
            <h2>Step 1: Upload Target Resume</h2>
            <FileUpload onFileSelect={handleTargetResumeSelect} mode="resume" />
            {targetResume && (
              <p className="selected-file">✓ Selected: {targetResume.name}</p>
            )}
          </div>

          <div className="upload-section">
            <h2>Step 2: Upload Reference Template (ZS/KPMG DOC/PDF/PPT)</h2>
            <FileUpload onFileSelect={handleTemplateSelect} mode="template" />
            {template && (
              <p className="selected-file">✓ Selected: {template.name}</p>
            )}
          </div>

          <button
            className="format-button"
            onClick={handleAnalyze}
            disabled={!targetResume || !template || loading}
          >
            {loading ? 'Analyzing...' : 'Step 3: Analyze & Get Suggestions'}
          </button>

          {workflowData && (
            <div className="result-section">
              <h3>Step 4: Review Suggestions {workflowData.atsScore ? `(ATS: ${workflowData.atsScore})` : ''}</h3>
              {workflowData.suggestions.length === 0 && (
                <p>No suggestions found. You can generate directly.</p>
              )}
              {workflowData.suggestions.map((s) => (
                <div key={s.id} className="suggestion-card">
                  <h4>{s.title}</h4>
                  <p><strong>Section:</strong> {s.section}</p>
                  <p><strong>Reason:</strong> {s.reason}</p>
                  {s.suggested_text && <p><strong>Suggested:</strong> {s.suggested_text}</p>}
                  <div className="suggestion-actions">
                    <button
                      className={`decision-button ${suggestionDecisions[s.id] === true ? 'active' : ''}`}
                      onClick={() => handleDecision(s.id, true)}
                    >
                      Accept
                    </button>
                    <button
                      className={`decision-button ${suggestionDecisions[s.id] === false ? 'active' : ''}`}
                      onClick={() => handleDecision(s.id, false)}
                    >
                      Reject
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}

          <button
            className="format-button"
            onClick={handleGenerate}
            disabled={!workflowData || !template || loading}
          >
            {loading ? 'Generating...' : 'Step 5: Generate Formatted Resume'}
          </button>

          {formattedFile && (
            <div className="success-section">
              <div className="success-content">
                <h3>✨ Your formatted resume is ready!</h3>
                <button
                  className="download-button"
                  onClick={downloadFile}
                >
                  📥 Download Formatted Resume
                </button>
              </div>
            </div>
          )}
        </div>
      </div>

      <footer className="footer">
        <p>&copy; 2024 Resume Formatter. Powered by Google Gemini & FastAPI.</p>
      </footer>
    </div>
  )
}

export default App
