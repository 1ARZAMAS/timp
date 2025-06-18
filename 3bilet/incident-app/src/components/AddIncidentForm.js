import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

function AddIncidentForm() {
  const [formData, setFormData] = useState({
    title: '',
    employee_id: '',
    status: 'Open'
  });
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('http://localhost:3001/incidents', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });
      
      if (response.ok) {
        navigate('/');
      } else {
        const error = await response.json();
        alert(error.error);
      }
    } catch (err) {
      console.error('Submit error:', err);
    }
  };

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  return (
    <div>
      <h2>Добавить инцидент</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Название:</label>
          <input
            name="title"
            value={formData.title}
            onChange={handleChange}
            required
          />
        </div>
        <div>
          <label>ID сотрудника:</label>
          <input
            name="employee_id"
            type="number"
            value={formData.employee_id}
            onChange={handleChange}
            required
          />
        </div>
        <div>
          <label>Статус:</label>
          <select
            name="status"
            value={formData.status}
            onChange={handleChange}
          >
            <option value="Open">Open</option>
            <option value="In Progress">In Progress</option>
            <option value="Closed">Closed</option>
          </select>
        </div>
        <button type="submit">Добавить</button>
      </form>
    </div>
  );
}

export default AddIncidentForm;