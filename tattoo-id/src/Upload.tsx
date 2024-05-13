import React, { useState } from 'react'
import './index.css'
import uploadLogo from '/upload.svg'
import './App.css'

function Upload() {
  const [files, setFiles] = useState<File[]>([])
  const [modelResults, setModelResults] = useState<string[]>([])

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const fileList = event.target.files
    if (fileList) {
      setFiles([...files, ...Array.from(fileList)])
    }
  }

  const handleDeleteFile = (fileToDelete: File) => {
    setFiles(files.filter((file) => file !== fileToDelete));
  };

  const handleRunModel = () => {
    // Add your code to connect to your ML model here
    // This function will be triggered when the "Run It" button is clicked
    console.log("Connecting to ML model...")
    const results = ["Result 1", "Result 2", "Result 3"]
    setModelResults(results)
  }

  return (
    <>
      <h1>Upload Your Photos/Videos with Tattoos</h1>
      <div>
        <a target="_blank">
          <img src={uploadLogo} className="logo" alt="Upload logo" />
        </a>
      </div>
      <div className="card">
        <input type="file" multiple onChange={handleFileChange} />
        <div>
          <ul>
            {files.map((file) => (
              <li key={file.name}>
                {file.name} - {file.size} bytes
                <button onClick={() => handleDeleteFile(file)}>Delete</button>
              </li>
            ))}
          </ul>
        </div>
      </div>
      <p className="read-the-docs">
        Upload your photos or videos you want to identify tattoos with criminal activities inside, <br />
        and click "Run Model" button below to run our model, <br />
        then you will find the results below.
      </p>
      <button onClick={handleRunModel}>Run Model</button>
      <div className="model-results">
        <h2>Model Results:</h2>
        <ul>
          {modelResults.map((result, index) => (
            <li key={index}>{result}</li>
          ))}
        </ul>
      </div>
    </>
  )
}

export default Upload
