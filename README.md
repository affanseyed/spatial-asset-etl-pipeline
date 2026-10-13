# Automated Spatial Infrastructure ETL & PostGIS Asset Pipeline

An open-source spatial ETL pipeline built with **Python (GeoPandas, OSMnx)** and **PostgreSQL/PostGIS** to ingest municipal road vector networks, clean spatial geometries, reproject to local UTM metric CRS (EPSG:32640), and map attributes into an **ISO 55000-compliant** asset management schema.

## Architecture Flow
1. **Extract**: Fetch vector features for municipal road infrastructure via OpenStreetMap Overpass APIs.
2. **Transform**: Geometry topology validation (`make_valid`), SRS reprojection to metric EPSG:32640 for exact length calculations, and ISO 55000 attribute enrichment (`asset_id`, `condition_score`).
3. **Load**: High-performance spatial table ingestion into PostGIS using SQLAlchemy and GeoAlchemy2.
4. **Analyze**: Spatial SQL queries leveraging PostGIS spatial indexing (`ST_DWithin`, `ST_Distance`).

## Tech Stack
* **Database**: PostgreSQL + PostGIS 
* **Language & ETL**: Python (GeoPandas, OSMnx, Shapely, PyPROJ)
* **ORM & Driver**: SQLAlchemy, GeoAlchemy2, Psycopg2