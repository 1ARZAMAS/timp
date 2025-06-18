import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';

function IncidentList() {
  const [incidents, setIncidents] = useState([]);
  const [loading, setLoading] = useState(true);
  const { employeeId } = useParams();
  const navigate = useNavigate();

  useEffect(() => {
    fetch(`http://localhost:3001/incidents?employee_id=${employeeId || ''}`)
      .then(res => res.json())
      .then(data => {
        setIncidents(data);
        setLoading(false);
      });
  }, [employeeId]);

  const handleDelete = async (id) => {
    try {
      const response = await fetch(`http://localhost:3001/incidents/${id}`, {
        method: 'DELETE'
      });
      
      if (response.status === 204) {
        setIncidents(incidents.filter(inc => inc.id !== id));
      } else {
        const error = await response.json();
        alert(error.error);
      }
    } catch (err) {
      console.error('Delete error:', err);
    }
  };

  if (loading) return <div>Loading...</div>;

  return (
    <div>
      <h2>Список инцидентов {employeeId && `для сотрудника ${employeeId}`}</h2>
      <button onClick={() => navigate('/add')}>Добавить инцидент</button>
      
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Название</th>
            <th>Статус</th>
            <th>Действия</th>
          </tr>
        </thead>
        <tbody>
          {incidents.map(inc => (
            <tr key={inc.id}>
              <td>{inc.id}</td>
              <td>{inc.title}</td>
              <td>{inc.status}</td>
              <td>
                <button 
                  onClick={() => handleDelete(inc.id)}
                  disabled={inc.status !== 'Closed'}
                >
                  Удалить
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default IncidentList;