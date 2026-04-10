import React, { useState } from 'react'
import './App.css'
import { FileUpload } from './FileUpload'
import { formatResume, parseResume, suggestImprovements } from './api'

export function App() {
  const [targetResume, setTargetResume] = useState(null)
  const [template, setTemplate] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [success, setSuccess] = useState(false)
  const [formattedFile, setFormattedFile] = useState(null)
  const [activeTab, setActiveTab] = useState('formatter')
  const [parseResult, setParseResult] = useState(null)
  const [improvements, setImprovements] = useState(null)

  const handleTargetResumeSelect = (file) => {
    setTargetResume(file)
    setError(null)
  }

  const handleTemplateSelect = (file) => {
    setTemplate(file)
    setError(null)
  }

  const handleFormat = async () => {
    if (!targetResume || !template) {
      setError('Please select both a target resume and a template')
      return
    }

    setLoading(true)
    setError(null)
    setSuccess(false)

    try {
      const formattedBlob = await formatResume(targetResume, template)
      
      // Create a blob URL for download
      const url = window.URL.createObjectURL(formattedBlob)
      
      setFormattedFile({
        name: 'formatted_resume.docx',
        url: url
      })
      
      setSuccess(true)
    } catch (err) {
      if (err.response?.data instanceof Blob) {
        try {
          const errorText = await err.response.data.text()
          const parsedError = JSON.parse(errorText)
          setError(parsedError.detail || 'Error formatting resume')
        } catch {
          setError('Error formatting resume')
        }
      } else {
        setError(err.response?.data?.detail || err.message || 'Error formatting resume')
      }
      console.error('Error:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleParseResume = async () => {
    if (!targetResume) {
      setError('Please select a resume to parse')
      return
    }

    setLoading(true)
    setError(null)

    try {
      const result = await parseResume(targetResume)
      setParseResult(result)
    } catch (err) {
      setError(err.response?.data?.detail || 'Error parsing resume')
      console.error('Error:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleGetSuggestions = async () => {
    if (!targetResume) {
      setError('Please select a resume')
      return
    }

    setLoading(true)
    setError(null)

    try {
      const result = await suggestImprovements(targetResume)
      setImprovements(result)
    } catch (err) {
      setError(err.response?.data?.detail || 'Error getting suggestions')
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
        <div className="tabs">
          <button 
            className={`tab ${activeTab === 'formatter' ? 'active' : ''}`}
            onClick={() => setActiveTab('formatter')}
          >
            Format Resume
          </button>
          <button 
            className={`tab ${activeTab === 'parser' ? 'active' : ''}`}
            onClick={() => setActiveTab('parser')}
          >
            Parse Resume
          </button>
          <button 
            className={`tab ${activeTab === 'suggestions' ? 'active' : ''}`}
            onClick={() => setActiveTab('suggestions')}
          >
            Suggestions
          </button>
        </div>

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

        {activeTab === 'formatter' && (
          <div className="formatter-section">
            <div className="upload-section">
              <h2>Step 1: Upload Target Resume</h2>
              <FileUpload onFileSelect={handleTargetResumeSelect} />
              {targetResume && (
                <p className="selected-file">✓ Selected: {targetResume.name}</p>
              )}
            </div>

            <div className="upload-section">
              <h2>Step 2: Upload Reference Template</h2>
              <FileUpload onFileSelect={handleTemplateSelect} />
              {template && (
                <p className="selected-file">✓ Selected: {template.name}</p>
              )}
            </div>

            <button 
              className="format-button"
              onClick={handleFormat}
              disabled={!targetResume || !template || loading}
            >
              {loading ? 'Processing...' : 'Format Resume'}
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
        )}

        {activeTab === 'parser' && (
          <div className="parser-section">
            <div className="upload-section">
              <h2>Upload Resume to Parse</h2>
              <FileUpload onFileSelect={handleTargetResumeSelect} />
              {targetResume && (
                <p className="selected-file">✓ Selected: {targetResume.name}</p>
              )}
            </div>

            <button 
              className="format-button"
              onClick={handleParseResume}
              disabled={!targetResume || loading}
            >
              {loading ? 'Parsing...' : 'Parse Resume'}
            </button>

            {parseResult && (
              <div className="result-section">
                <h3>Parsed Resume Data</h3>
                <pre className="result-json">
                  {JSON.stringify(parseResult, null, 2)}
                </pre>
              </div>
            )}
          </div>
        )}

        {activeTab === 'suggestions' && (
          <div className="suggestions-section">
            <div className="upload-section">
              <h2>Upload Resume for Suggestions</h2>
              <FileUpload onFileSelect={handleTargetResumeSelect} />
              {targetResume && (
                <p className="selected-file">✓ Selected: {targetResume.name}</p>
              )}
            </div>

            <button 
              className="format-button"
              onClick={handleGetSuggestions}
              disabled={!targetResume || loading}
            >
              {loading ? 'Analyzing...' : 'Get Suggestions'}
            </button>

            {improvements && (
              <div className="result-section">
                <h3>Improvement Suggestions</h3>
                <pre className="result-json">
                  {JSON.stringify(improvements, null, 2)}
                </pre>
              </div>
            )}
          </div>
        )}
      </div>

      <footer className="footer">
        <p>&copy; 2024 Resume Formatter. Powered by Google Gemini & FastAPI.</p>
      </footer>
    </div>
  )
}

export default App
