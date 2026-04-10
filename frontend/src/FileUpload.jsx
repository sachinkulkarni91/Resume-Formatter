import React, { useCallback } from 'react'
import { useDropzone } from 'react-dropzone'
import './FileUpload.css'

export const FileUpload = ({ onFileSelect, language = 'en' }) => {
  const translations = {
    en: {
      dropText: 'Drag and drop your files here, or click to select',
      buttonText: 'Select Files',
      supportedFormats: 'Supported formats: PDF, DOCX, DOC'
    },
    es: {
      dropText: 'Arrastra y suelta tus archivos aquí, o haz clic para seleccionar',
      buttonText: 'Seleccionar archivos',
      supportedFormats: 'Formatos soportados: PDF, DOCX, DOC'
    }
  }

  const t = translations[language] || translations.en

  const onDrop = useCallback(acceptedFiles => {
    if (acceptedFiles.length > 0) {
      onFileSelect(acceptedFiles[0])
    }
  }, [onFileSelect])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
      'application/msword': ['.doc']
    }
  })

  return (
    <div {...getRootProps()} className={`file-upload ${isDragActive ? 'active' : ''}`}>
      <input {...getInputProps()} />
      <div className="upload-content">
        <div className="upload-icon">📄</div>
        <p>{t.dropText}</p>
        <button className="upload-button">{t.buttonText}</button>
        <p className="supported-formats">{t.supportedFormats}</p>
      </div>
    </div>
  )
}
