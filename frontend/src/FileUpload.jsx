import React, { useCallback } from 'react'
import { useDropzone } from 'react-dropzone'
import './FileUpload.css'

export const FileUpload = ({ onFileSelect, language = 'en', mode = 'resume' }) => {
  const translations = {
    en: {
      dropText: 'Drag and drop your files here, or click to select',
      buttonText: 'Select Files',
      supportedFormatsResume: 'Supported formats: PDF, DOCX, DOC',
      supportedFormatsTemplate: 'Supported formats: PDF, DOCX, DOC, PPT, PPTX'
    },
    es: {
      dropText: 'Arrastra y suelta tus archivos aquí, o haz clic para seleccionar',
      buttonText: 'Seleccionar archivos',
      supportedFormatsResume: 'Formatos soportados: PDF, DOCX, DOC',
      supportedFormatsTemplate: 'Formatos soportados: PDF, DOCX, DOC, PPT, PPTX'
    }
  }

  const t = translations[language] || translations.en

  const onDrop = useCallback(acceptedFiles => {
    if (acceptedFiles.length > 0) {
      onFileSelect(acceptedFiles[0])
    }
  }, [onFileSelect])

  const acceptedFileTypes = mode === 'template'
    ? {
        'application/pdf': ['.pdf'],
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
        'application/msword': ['.doc'],
        'application/vnd.openxmlformats-officedocument.presentationml.presentation': ['.pptx'],
        'application/vnd.ms-powerpoint': ['.ppt']
      }
    : {
        'application/pdf': ['.pdf'],
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
        'application/msword': ['.doc']
      }

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: acceptedFileTypes
  })

  return (
    <div {...getRootProps()} className={`file-upload ${isDragActive ? 'active' : ''}`}>
      <input {...getInputProps()} />
      <div className="upload-content">
        <div className="upload-icon">📄</div>
        <p>{t.dropText}</p>
        <button className="upload-button">{t.buttonText}</button>
        <p className="supported-formats">{mode === 'template' ? t.supportedFormatsTemplate : t.supportedFormatsResume}</p>
      </div>
    </div>
  )
}
