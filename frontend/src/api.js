import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8005'

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'multipart/form-data'
  }
})

export const formatResume = async (targetResume, template) => {
  const formData = new FormData()
  formData.append('target_resume', targetResume)
  formData.append('template', template)

  const response = await api.post('/api/format-resume', formData, {
    responseType: 'blob'
  })
  return response.data
}

export const formatFromParsed = async (parsedData, template) => {
  const formData = new FormData()
  formData.append('parsed_json', JSON.stringify(parsedData))
  formData.append('template', template)

  const response = await api.post('/api/format-from-parsed', formData, {
    responseType: 'blob'
  })
  return response.data
}

export const parseResume = async (resume) => {
  const formData = new FormData()
  formData.append('resume', resume)

  const response = await api.post('/api/parse-resume', formData)
  return response.data
}

export const extractTemplate = async (template) => {
  const formData = new FormData()
  formData.append('template', template)

  const response = await api.post('/api/extract-template', formData)
  return response.data
}

export const suggestImprovements = async (resume) => {
  const formData = new FormData()
  formData.append('resume', resume)

  const response = await api.post('/api/suggest-improvements', formData)
  return response.data
}
