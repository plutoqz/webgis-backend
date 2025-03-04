const express = require('express');
const { Pool } = require('pg');
const cors = require('cors');

const app = express();
app.use(cors());
app.use(express.json());

// 数据库配置
const pool = new Pool({
  user: 'postgres',
  host: 'localhost',
  database: 'webgis_db',
  password: '245011058',
  port: 5432,
});

// 获取所有要素（GeoJSON格式）
app.get('/api/features', async (req, res) => {
  try {
    const query = `
      SELECT 
        id,
        name,
        ST_AsGeoJSON(geom)::json AS geometry,
        properties
      FROM gis_features
    `;
    const { rows } = await pool.query(query);
    res.json({
      type: "FeatureCollection",
      features: rows.map(row => ({
        type: "Feature",
        geometry: row.geometry,
        properties: {
          id: row.id,
          name: row.name,
          ...row.properties
        }
      }))
    });
  } catch (err) {
    console.error(err);
    res.status(500).send('Server Error');
  }
});

// 添加新要素
app.post('/api/features', async (req, res) => {
  const { geometry, properties } = req.body;
  
  try {
    const query = `
      INSERT INTO gis_features (name, geom, properties)
      VALUES ($1, ST_SetSRID(ST_GeomFromGeoJSON($2), 4326), $3)
      RETURNING *
    `;
    const values = [
      properties.name || 'Unnamed Feature',
      JSON.stringify(geometry),
      properties
    ];
    
    const { rows } = await pool.query(query, values);
    res.status(201).json(rows[0]);
  } catch (err) {
    console.error(err);
    res.status(500).send('Server Error');
  }
});

app.listen(5000, () => console.log('Server running on port 5000'));
