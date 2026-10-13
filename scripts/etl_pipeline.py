import geopandas as gpd
import osmnx as ox
from sqlalchemy import create_engine
from sqlalchemy.engine import URL

print("1. Fetching municipal road network vector data...")
# Fetching features for Downtown Dubai
place_name = "Downtown Dubai, United Arab Emirates"
gdf_raw = ox.features_from_place(place_name, tags={"highway": True})

print("2. Cleaning geometries and applying ISO 55000 asset schema...")
# Keep linear geometries & make geometries valid
gdf_clean = gdf_raw[gdf_raw.geometry.type.isin(["LineString", "MultiLineString"])].copy()
gdf_clean["geometry"] = gdf_clean["geometry"].make_valid()

# Reproject to UTM Zone 40N (EPSG:32640 for UAE) to calculate accurate length in meters
gdf_projected = gdf_clean.to_crs(epsg=32640)
gdf_projected["length_meters"] = gdf_projected.geometry.length

# Enrich with ISO 55000 metadata
gdf_projected["asset_id"] = ["AST-" + str(i).zfill(6) for i in range(len(gdf_projected))]
gdf_projected["asset_type"] = gdf_projected["highway"].fillna("unclassified").astype(str)
gdf_projected["installation_year"] = 2021
gdf_projected["condition_score"] = 4

# Select target schema columns
columns_to_keep = ["asset_id", "asset_type", "installation_year", "condition_score", "length_meters", "geometry"]
gdf_final = gdf_projected[columns_to_keep]

print("3. Loading vector data into PostGIS...")
DB_USER = "postgres"
DB_PASS = "Signmeup@123"  # <--- REPLACE THIS WITH YOUR POSTGRESQL PASSWORD
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "infrastructure_db"

# Safely build database connection URL handling special characters (@, #, $, etc.)
connection_url = URL.create(
    "postgresql+psycopg2",
    username=DB_USER,
    password=DB_PASS,
    host=DB_HOST,
    port=DB_PORT,
    database=DB_NAME,
)

engine = create_engine(connection_url)

gdf_final.to_postgis(
    name="municipal_road_assets",
    con=engine,
    if_exists="replace",
    index=False,
    schema="public"
)

print("\nSUCCESS: Spatial ETL pipeline complete! Data loaded into PostGIS.")