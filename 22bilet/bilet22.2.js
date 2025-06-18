app.post('/upload', async (req, res) => {
  try {
    if (!req.file) {
      return res.status(400).json({ success: false, error: 'Файл не был загружен.' });
    }
    // Сохранение информации о файле в БД
    const { originalname, mimetype, size, filename, path } = req.file;
    const query = `
      INSERT INTO reports (original_name, mime_type, file_size, file_name, file_path, created_at)
      VALUES ($1, $2, $3, $4, $5, NOW())
      RETURNING id;
    `;
    const result = await pool.query(query, [originalname, mimetype, size, filename, path]);

    res.status(201).json({ 
      success: true,
      message: 'Файл успешно загружен.',
      fileId: result.rows[0].id,
      fileName: filename
    });

  } catch (error) {
    console.error('Ошибка загрузки:', error);
    res.status(500).json({ success: false, error: error.message });
  }
});
