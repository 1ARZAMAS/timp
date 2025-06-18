import React from 'react';
import { Routes, Route, Link } from 'react-router-dom';
import IncidentList from './components/IncidentList';
import AddIncidentForm from './components/AddIncidentForm';

function App() {
  return (
    <div style={{ padding: '20px' }}>
      <nav>
        <Link to="/">Все инциденты</Link> | 
        <Link to="/employee/101">Инциденты сотрудника 101</Link> | 
        <Link to="/add">Добавить инцидент</Link>
      </nav>

      <Routes>
        <Route path="/" element={<IncidentList />} />
        <Route path="/employee/:employeeId" element={<IncidentList />} />
        <Route path="/add" element={<AddIncidentForm />} />
      </Routes>
    </div>
  );
}

export default App;