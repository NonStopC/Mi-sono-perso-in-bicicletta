import { useState, useEffect } from 'react'
import axios from 'axios'
import './App.css'

const API_URL = 'http://localhost:8080'

function App() {
  const [utenti, setUtenti] = useState([])
  const [nuovoNome, setNuovoNome] = useState('')

  // Carica utenti all'avvio
  useEffect(() => {
    fetchUtenti()
  }, [])

  const fetchUtenti = async () => {
    try {
      const response = await axios.get(`${API_URL}/utenti/`)
      setUtenti(response.data)
    } catch (error) {
      console.error('Errore nel caricamento:', error)
    }
  }

  const creaUtente = async (e) => {
    e.preventDefault()
    try {
      await axios.post(`${API_URL}/utenti/`, { nome: nuovoNome })
      setNuovoNome('')
      fetchUtenti()
    } catch (error) {
      console.error('Errore nella creazione:', error)
    }
  }

  const eliminaUtente = async (id) => {
    try {
      await axios.delete(`${API_URL}/utenti/${id}`)
      fetchUtenti()
    } catch (error) {
      console.error('Errore nella cancellazione:', error)
    }
  }

  return (
    <div className="App">
      <h1>Gestione Biciclette</h1>
      
      {/* Form creazione utente */}
      <form onSubmit={creaUtente}>
        <input
          type="text"
          placeholder="Nome utente"
          value={nuovoNome}
          onChange={(e) => setNuovoNome(e.target.value)}
          required
        />
        <button type="submit">Aggiungi Utente</button>
      </form>

      {/* Lista utenti */}
      <div>
        <h2>Utenti</h2>
        {utenti.map(utente => (
          <div key={utente.id} style={{ margin: '10px', padding: '10px', border: '1px solid #ccc' }}>
            <p><strong>{utente.nome}</strong> (ID: {utente.id})</p>
            <p>Biciclette: {utente.biciclette.length}</p>
            <button onClick={() => eliminaUtente(utente.id)}>Elimina</button>
          </div>
        ))}
      </div>
    </div>
  )
}

export default App
