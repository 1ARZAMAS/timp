class IncidentDAL:
    """Слой доступа к данным для работы с инцидентами"""
    
    def __init__(self, db_connection):
        self.db = db_connection

    def insert_incident(self, title, threat_level, description, reporter_id, status):
        query = """
        INSERT INTO incidents (title, threat_level, description, reporter_id, status, created_at) 
        VALUES (%s, %s, %s, %s, %s, NOW()) 
        RETURNING id;
        """
        result = self.db.execute(query, (title, threat_level, description, reporter_id, status))
        return result.fetchone()[0]

    def get_incident_by_id(self, incident_id):
        query = """
        SELECT id, title, threat_level, description, status, created_at, closed_at 
        FROM incidents 
        WHERE id = %s;
        """
        result = self.db.execute(query, (incident_id,))
        return result.fetchone()

    def update_incident_status(self, incident_id, status):
        query = """
        UPDATE incidents 
        SET status = %s, closed_at = CASE WHEN %s = 'closed' THEN NOW() ELSE NULL END 
        WHERE id = %s;
        """
        self.db.execute(query, (status, status, incident_id))

    def get_incidents_by_status_and_threat(self, status, min_threat):
        # Предполагаем, что threat_level хранится как enum или имеет числовые эквиваленты
        threat_order = {'low': 1, 'medium': 2, 'high': 3, 'critical': 4}
        min_threat_value = threat_order[min_threat]
        
        query = """
        SELECT id, title, threat_level, description, status, created_at 
        FROM incidents 
        WHERE status = %s 
        AND CASE threat_level
            WHEN 'low' THEN 1
            WHEN 'medium' THEN 2
            WHEN 'high' THEN 3
            WHEN 'critical' THEN 4
        END >= %s
        ORDER BY created_at DESC;
        """
        result = self.db.execute(query, (status, min_threat_value))
        return result.fetchall()

    def get_incident_measures(self, incident_id):
        query = """
        SELECT id, description, status, created_at, completed_at 
        FROM incident_measures 
        WHERE incident_id = %s;
        """
        result = self.db.execute(query, (incident_id,))
        return result.fetchall()


class IncidentService:
    """Слой бизнес-логики для работы с инцидентами"""
    
    def __init__(self, dal):
        self.dal = dal

    def create_incident(self, data):
        # Проверка данных
        if not all(field in data for field in ['title', 'threat_level', 'description', 'reporter_id']):
            raise ValueError("Missing required fields")
        
        if data['threat_level'] not in ['low', 'medium', 'high', 'critical']:
            raise ValueError("Invalid threat level")
        
        # Создание инцидента через DAL
        incident_id = self.dal.insert_incident(
            title=data['title'],
            threat_level=data['threat_level'],
            description=data['description'],
            reporter_id=data['reporter_id'],
            status='open'
        )
        
        return self.dal.get_incident_by_id(incident_id)

    def close_incident(self, incident_id):
        incident = self.dal.get_incident_by_id(incident_id)
        if not incident:
            raise ValueError("Incident not found")
        
        if incident['status'] == 'closed':
            raise ValueError("Incident already closed")
        
        measures = self.dal.get_incident_measures(incident_id)
        if not measures:
            raise ValueError("No measures taken for this incident")
        
        if any(m['status'] != 'completed' for m in measures):
            raise ValueError("Not all measures are completed")
        
        self.dal.update_incident_status(incident_id, 'closed')
        return self.dal.get_incident_by_id(incident_id)

    def get_open_incidents_by_threat(self, min_threat_level):
        if min_threat_level not in ['low', 'medium', 'high', 'critical']:
            raise ValueError("Invalid threat level")
        
        return self.dal.get_incidents_by_status_and_threat('open', min_threat_level)

